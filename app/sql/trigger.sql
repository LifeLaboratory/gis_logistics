
CREATE OR REPLACE FUNCTION insert_transaction_bus()
  RETURNS TRIGGER AS  $$
BEGIN

  if new.id_halt is null then

    new.id_route = coalesce(
      (
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
  where 
    input > 0
    and weight > 0
    and count_halt > 0
    and outcome > 0
    and output > 0
  group by
      tn.id_route
) tn
),
max_coef as (
  select max(coef)
  from agr
),
select_route as (
  select 
    case 
      when max - (select coef from agr where id_route = new.id_route limit 1) > 0.5 and (select count(1) from bus where id_route = 2) > 1 then (select id_route from agr where coef = max limit 1)
      else null
    end::int as id_route
  from agr
    left join max_coef on true
  limit 1
)
      select * from select_route limit 1),
      (select next_route 
      from route
      where id_route = new.id_route 
      limit 1)
    );  
    
    update bus --+
    set id_route = new.id_route
    where id_bus = new.id_bus;
      
    insert into flight(id_bus, id_route) --+
    values(new.id_bus, new.id_route);
    
    new.output = new.outcome;
    
    new.outcome = 0;
    --new.time = now();
    /*new.id_flight = (
      select id_flight 
      from flight 
      where id_bus = new.id_bus 
        and id_route = new.id_route
      order by 
	id_flight desc
      limit 1
    );*/
 /* else
    new.id_flight = (
      select id_flight 
      from flight 
      where id_bus = new.id_bus 
        and id_route = new.id_route
      order by id_flight desc
      limit 1
    );*/
  end if;
  return new;
END;
$$ LANGUAGE 'plpgsql';


DROP TRIGGER insert_transaction ON public.transaction;

CREATE TRIGGER insert_transaction
  BEFORE insert
  ON public.transaction
  FOR EACH ROW
  EXECUTE PROCEDURE public.insert_transaction_bus();
