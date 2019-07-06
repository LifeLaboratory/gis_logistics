from app.base.sql import Sql


class Bus:
    @staticmethod
    def get_all_bus_info():
        query = '''
select 
  bus.id_bus
  , bus.id_route
  , rh.id_halt
  , bus.weight
  , tn.input
  , tn.output
  , tn.outcome
  , tn.time::text
  , rh.next_halt
  , rh.next_time::text
from bus bus
  left join lateral (
  select *
  from transaction tn 
  where (bus.id_bus, bus.id_route) = (tn.id_bus, tn.id_route)
  order by id_trunc desc
  limit 1
 ) tn on true
 left join route_halt rh on (rh.id_route, rh.id_halt) = (tn.id_route, tn.id_halt)
        '''
        return Sql.exec(query)

    @staticmethod
    def get_one_bus_info(id_bus):
        query = '''
select
  id_route
  , id_bus
  , sum(input)
from transaction 
where id_bus = {id_bus}
group by 
  id_route
  , id_bus
        '''.format(id_bus=id_bus)
        return Sql.exec(query)

    @staticmethod
    def insert_bus_transaction(param):
        query = '''
insert into transaction(id_bus, id_route, id_halt, input, output, outcome, time)
select 
  data.id_bus
  , data.id_route
  , coalesce(tn.next_halt, (select id_halt from route_halt rh where rh.id_route = data.id_route order by id_halt limit 1))
  , data.input
  , data.output
  , coalesce( 
      case 
        when coalesce(outcome, 0) - data.output + data.input < 0 then 0
        else coalesce(outcome, 0) - data.output + data.input
      end
    , 0)
  , coalesce(coalesce(tn.time, now()) + tn.next_time)
from (
  select 
      {id_bus} as id_bus
    , {id_route} as id_route
    , {input} as input
    , {output} as output
) data
 left join (
  select *
    , coalesce(
        rh.next_halt, 
        (select id_halt 
         from route_halt rh2 
         where rh2.id_route = {id_route} 
         order by id_halt 
         limit 1
         )
      ) as new_halt
  
  from transaction tn
    left join route_halt rh on (rh.id_route, rh.id_halt) = (tn.id_route, tn.id_halt)
  where tn.id_route = {id_route} 
    and tn.id_bus = {id_bus}
    and next_halt is not null
  order by 
    tn.id_trunc desc
  limit 1
) tn on true
'''.format(**param)
        return Sql.exec(query)

    @staticmethod
    def insert_bus(param):
        query = '''
insert into bus(id_bus, id_route, x, y, class, weight)
select 
  {id_bus}
  , {id_route}
  , {x}
  , {y}
  , {class}
  , {weight}
'''.format(**param)
        return Sql.exec(query)

    @staticmethod
    def update_bus(param):
        query = '''
update bus(id_bus, id_route, x, y, class, weight)
set dire
select 
  {id_bus}
  , {id_route}
  , {x}
  , {y}
  , {class}
  , {weight}
'''.format(**param)
        return Sql.exec(query)
