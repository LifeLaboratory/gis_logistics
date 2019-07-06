from app.base.sql import Sql


class Route:
    def get_all_route_bus(self):
        query = '''
select *
from route
  left join bus using(id_route)
order by 
  id_route
  , id_bus
'''
        return Sql.exec(query)

    def coef_route(self):
        query = '''
with agr as (
select 
    id_route
  , input / count_bus as input
  , outcome_1
  , outcome_2
  , output / count_bus as output
  , input / count_bus * 0.7 + outcome_1 * 1 + outcome_2 * 0.6 + output / count_bus * 0.5 as coef
from (
  select
      tn.id_route
     , sum(input::double precision / weight::double precision / count_halt::double precision) as input
     , sum(case when outcome = weight then 1 else 0 end::double precision / count_halt::double precision) as outcome_1
     , sum(case when outcome > weight * 0.8 then 1 else 0 end::double precision / count_halt::double precision) as outcome_2
     , sum(output / weight::double precision / count_halt::double precision) as output
     , count(distinct tn.id_bus) as count_bus
  from transaction tn
    left join bus on (bus.id_route, bus.id_bus) = (tn.id_route, tn.id_bus)
    left join lateral (
      select 
        count(1) as count_halt
      from transaction rh
      where rh.id_route = tn.id_route 
        and rh.id_flight = tn.id_flight
    ) ch on true
  group by
      tn.id_route
) tn
),
max_coef as (
  select max(coef)
  from agr
)
  select 
    case 
      when max - (select coef from agr where id_route = {id_route} limit 1) > 0.5 and (select count(1) from bus where id_route = 2) > 1 then (select id_route from agr where coef = max limit 1)
      else {id_route}
    end as id_route
  from agr
    left join max_coef on true
  limit 1
'''.format()