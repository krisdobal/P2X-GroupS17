clear; clc; close all;

spot = readtable('elspotprices.xlsx');
spotDK2 = readtable('elspotpricesDK2.xlsx');
wind5_1 = readtable('electricityprodex5minrealtimeJanJune.xlsx');
wind5_2 = readtable('electricityprodex5minrealtimeJulDec.xlsx');
wind5 = [wind5_1;wind5_2];

t1h = 0:1:length(spot.HourDK)-1;
t5m = 0:5/60:(length(wind5.Minutes5DK))*(5/60)-5/60;

plot(t1h,spot.SpotPriceDKK)
hold on
plot(t1h,spotDK2.SpotPriceDKK)

xlabel('time $[H]$','Interpreter','latex');
ylabel('Spotprice $[dkk]$','Interpreter','latex');

%hold on
%yyaxis right
%plot(t5m,wind5.OffshoreWindPower)
%ylabel('Windpower $[MW]$','Interpreter','latex');
title('spotprice and windpower production of 2021','Interpreter','latex');

% https://api.energidataservice.dk/datastore_search?resource_id=electricityprodex5minrealtime&limit=5
% {"query":"query Dataset {electricityprodex5minrealtime(where: {Minutes5UTC: {_gte: \"2021-01-01\", _lt: \"2022-01-01\"}PriceArea: {_eq: \"DK1\"}} order_by: {Minutes5UTC: asc} limit: 100 offset: 0){Minutes5UTC Minutes5DK PriceArea ProductionLt100MW ProductionGe100MW OffshoreWindPower OnshoreWindPower SolarPower ExchangeGreatBelt ExchangeGermany ExchangeNetherlands ExchangeNorway ExchangeSweden BornholmSE4 }}"}
%figure()
%plot(t5,
%import urllib.request
%url = 'https://api.energidataservice.dk/datastore_search?resource_id=electricityprodex5minrealtime&limit=5'
%fileobj = urllib.request.urlopen(url)
%print(fileobj.read())

