from app.base.sql import Sql


class Route:
    def get_all_route_bus(self):
        query = '''
select 
   end_x as end_y 
  , end_y as end_x
  , name
  , start_x as start_y
  , start_y as start_x
  , id_route
  , case 
      when bus.weight * 0.8 > tn.outcome then 5
      else 1
    end as "Индикация"
from route r 
  left join bus using(id_route)
   left join lateral (
   select outcome
   from transaction tn
   where tn.id_route = r.id_route
   order by id_trunc
   limit 1
 ) tn on true
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
),
select_route (
  select 
    case 
      when max - (select coef from agr where id_route = {id_route} limit 1) > 0.5 and (select count(1) from bus where id_route = 2) > 1 then (select id_route from agr where coef = max limit 1)
      else {id_route}
    end as id_route
  from agr
    left join max_coef on true
  limit 1
)
table select_route
'''.format(id_route=1)
        return Sql.exec(query)

    @staticmethod
    def get_route_list(id_route):
        query = '''
select x, y
from route_halt
  left join halt using(id_halt)
where id_route = {id_route}
  and id_halt % 2 = 0
order by id_halt nulls last
limit 23
'''.format(id_route=id_route)
        x_y = Sql.exec(query)
        query = '''
select *
  , case 
      when bus.weight * 0.8 > tn.outcome then 5
      else 1
    end as "Индикация"
from route r
 left join lateral (
   select id_bus, outcome
   from transaction tn
   where tn.id_route = r.id_route
   order by id_trunc
   limit 1
 ) tn on true
 left join bus bus on bus.id_bus = tn.id_bus
where r.id_route = {id_route}
'''.format(id_route=id_route)
        x_y_average = Sql.exec(query)
        point = x_y_average[0]
        x = [elem.get('x') for elem in x_y]
        y = [elem.get('y') for elem in x_y]
        data = {
            'start': '{},{}'.format(point.get('start_y'), point.get('start_x')),
            'end': '{},{}'.format(point.get('end_y'), point.get('end_x')),
            'waypoints_x': y,
            'waypoints_y': x,
            'индикация': point.get('Индикация')
        }
        return data