create view years as select 2016+a from
(select 0 as a union select 1 union select 2 union select 3 union select 4 union select 5 union select 6 union select 7 union select 8 union select 9);
