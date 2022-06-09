%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Power-to-X in Power systens  - June 2022
%%%
%%% Alessandro Singlitico, Researcher at DTU Wind and Energy Systems
%%%
%%% Extracted and simplified from:
%%% Singlitico A, Østergaard J, Chatzivasileiadis S. Onshore, offshore or in-turbine electrolysis? 
%%% Techno-economic overview of alternative integration designs for green hydrogen production into 
%%% Offshore Wind Power Hubs. Renew Sustain Energy Transit 2021;1:100005. doi:10.1016/j.rset.2021.100005.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% cleaning up variable and closing open windows
clc
clear
close all

%% EXERCISE 1 - investemnt cost comparison HVDC transmission vs hydrogen pipeline


%%% Input values

Z=1;               % [-] assumption ideal gas
Tbase = 288.15;    % [K] standard temperature        
Pbase = 101325; % [Pa] standard pressure
Tmed = 285.15;     % [K] mean temperature
Ggas = 0.0696;     % [-] gas gravity
roug =0.05;        % roughness of the pipeline [mm]
dynvisH2=8.64e-6;  % dynamic vyscosity [kg/m s] 15C 1atm Pa*s
Rconst =  8.314;   % Univeral gas constant [kJ/(kmol K)]
Vout= 0.3387;       % Mole volume [m3/kmol] 70bar
RhoH2out = 5.9519;  %density [kg/m3]at 70 bar
pout = 70;         % Pressure onshore [bar]
Dbase= 0.0841;     % density [kg/m3]at standard conditions
LHV = 33.3;        %[kWh/kg] lower heating value hydrogen
eff_electro = 0.68; %efficiency electrolyser
pin_comp= 30;        % output pressure of the electrolyser [bar]
compr_cost = 3000;   %M€/GW
compr_eff = 0.5;    %efficiencty of the compressor [-]
gamma_comp = 1.4074; %cp/cv for hydrogen
pout_comp_on=70;    % [bar] pressure of the hydrogen delivered onshore

%%% variable initialisation

i=1; %flag variable
k=1; %flag variable

maxL= 500; %assumed maximum distance [km]
minL= 100; %assumed min distance [km]

maxP=20; %assumed maximum capacity [GW]
minP= 1; %assumed minimum capacity [GW]

step = 19; %number of steps assumed in the iteration

Li = [minL:(maxL-minL)/step:maxL];
Pi = [minP:(maxP-minP)/step:maxP];


%%% Calculation investment cost HVDC transmission


for L = minL:(maxL-minL)/step:maxL  
    
for P =minP:(maxP-minP)/step:maxP 
nodes_on= 1;  %total number of nodes onshore
nodes_off=1;  % number of nodes offshore

Blp = 0.6;    % length-power dependent costs[M€/GWkm]
Bl = 1.345;   % lenght dependent costs[M€/km]
Bf = 0;       % fixed costs[M€]
Pmax = 2;     % max power [GW]

Np = 101;     % node power dependent costs [M€/GW]
Nf = 61.60;   % node fixed costs [M€]

Sp = 117.9;   % offshore node power dependent costs [M€/GW] EXCLUDING PLATFORM
Sf = 45.4;    % offshore node fixed costs [M€]

B = Blp*L*P + ceil(P/Pmax)*(Bl.*L+Bf); %capital cost of the cable [M€]
N = Np*P +  ceil(P/Pmax)*(Nf);         %capital cost of the onshore station [M€]
S = Sp*P +  ceil(P/Pmax)*(Sf);         % capital cost of the offshore station [M€]

Capex_HVDC(i,k) = B + nodes_on*N + nodes_off*S; % capital invesment for the HVDC system (including the two substations and the cable)[M€]
Capex_elect(i,k) = 450 * P;               %capital investment of the electrolyser

Q = P*1000000/LHV/Dbase*24*eff_electro; % nominal volumetric flow per day (m3/day)
m = P*1000000/LHV*eff_electro;          % nominal mass flow per hour [kg/h]

cons_compresmax_on(i,k) = m*286.76/Ggas*Tmed*(gamma_comp /(gamma_comp -1))*((pout_comp_on /pin_comp)^((gamma_comp-1)/gamma_comp)-1)/compr_eff/(3.6*10^12); % nominal power of the compressor [GW]
compres_inv_on(i,k) = compr_cost*cons_compresmax_on(i,k);% invenstment cost compressor [M€]


Capex_tot_on(i,k)= Capex_HVDC(i,k)+ Capex_elect(i,k)+compres_inv_on(i,k); %total invenstemnt cost for the transport to shore in the case of onshosre electrolyser

i=i+1;

end

i=1;
k=k+1;

end

%%% Investment cost for hydrogen pipeline %%%
i = 1;             %reset flag variable
k= 1;                %reset flag variable

u_erosout= 100*sqrt(Z*Rconst*Tmed/(29*0.0696*pout*10^2));  %erosional velocity [m/s] (maximum velocity allowed to avoid damage)
v_out = u_erosout*0.5; %velocity out

for L = minL:(maxL-minL)/step:maxL  
      
for P = [minP:(maxP-minP)/step:maxP] % max daily volume [m3/day]
 
    Q = P*1000000/LHV/Dbase*24*eff_electro; % nominal volumetric flow per day (m3/day)
    m = P*1000000/LHV*eff_electro;          %  nominal mass flow per hour (kg/h)

D=1001;
num_pipe=1;

    while D>1000    %it is assumed that a maximum of 1 m diameter pipeline can be manufactured, otherwhise the hydrogen flow is splitted
    Q = Q/num_pipe;    
    Areapipe= Q/24*Dbase/RhoH2out/(3600)/v_out;
    D = sqrt(Areapipe/pi*4)*1000; %[mm]

    num_pipe  =num_pipe+1;
    end
    
    if D<100   % If the diameter is inferior 100mm,  it is assumed that a 100m diameter pipeline is used, because of manufacturing reasons
        D=100;
    end

      num_pipe  =num_pipe-1;
      
Capex_pipe(i,k) = num_pipe*1.75*L*(0.314+0.574*10^-3*(D)+1.7*10^-6*(D)^2);  % the diameter is given in [mm]
Capex_elect(i,k) = 450 * P; %capex electrolyser (the onshore electrolyser might cost more due to installation costs but we assume that is the same as installing onshore for  simplifying it)

ReH2(i,k) = 0.5134*(Pbase/1000/Tbase)*(Ggas*Q)/(dynvisH2*10*D);
K = roug/D;
Lam = colebrook(ReH2(i,k),K);

pdrop = Q/(1.1494*10^(-3)*(Tbase/(Pbase/10^3))*sqrt(D^5/(Z*Tmed*Ggas*Lam*L))); %pressure drop 
pp(i,k)= pdrop; %[kPa]
pin = (pdrop^2 + (pout*101.325)^2)^(1/2)/101.325;

pout_comp = pin;
cons_compresmax(i,k) = m*286.76/Ggas*Tmed*(gamma_comp /(gamma_comp -1))*((pout_comp /pin_comp)^((gamma_comp-1)/gamma_comp)-1)/compr_eff/(3.6*10^12); % nominal capacity copressor [GW]
compres_inv(i,k) = compr_cost*cons_compresmax(i,k)*num_pipe ;% capex compressor [M€]

Capex_tot_off(i,k)= Capex_pipe(i,k) + Capex_elect(i,k) + compres_inv(i,k);  %no desalination is considered to simplify the exercise

i=i+1;

end

i=1;
k=k+1;

end

%%%%% ADD YOUR CODE HERE - YOU DONT NEED TO TOUCH THE PREVIOUS CODE %%%%%