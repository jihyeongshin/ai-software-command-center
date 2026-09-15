"""Public Live persistence, isolated from owner workflow authority.

The NOLOGIN runtime role has only reviewed function execution and safe reads.
Provisioning a login/credential and activating a campaign remain release actions.
An empty installation can be downgraded for migration tests. Any public liability
or journal forbids downgrade; use a forward correction instead.
"""

import sqlalchemy as sa
from alembic import op

revision = "20260915_0013"
down_revision = "20260914_0012"
branch_labels = None
depends_on = None

TABLES = (
    "public_control",
    "public_campaign",
    "public_day",
    "public_client",
    "public_run",
    "public_idempotency",
    "public_rate_event",
    "public_reservation",
    "public_slot",
    "public_outbox",
    "public_dispatch",
    "public_money_event",
    "public_observation",
)

DDL = """
CREATE SCHEMA public_live_api;
-- statement
CREATE TABLE public.public_campaign (
 campaign_id text PRIMARY KEY CHECK(length(campaign_id) BETWEEN 1 AND 128),
 starts_at timestamptz NOT NULL, ends_at timestamptz NOT NULL CHECK(ends_at>starts_at),
 limit_micro bigint NOT NULL DEFAULT 15000000 CHECK(limit_micro=15000000),
 available bigint NOT NULL CHECK(available>=0), held bigint NOT NULL DEFAULT 0 CHECK(held>=0),
 settled bigint NOT NULL DEFAULT 0 CHECK(settled>=0),
 hmac_version text NOT NULL, scenario_id text NOT NULL, scenario_version text NOT NULL,
 content_digest bytea NOT NULL CHECK(octet_length(content_digest)=32),
 policy_digest bytea NOT NULL CHECK(octet_length(policy_digest)=32),
 CHECK(available+held+settled=limit_micro)
);
-- statement
CREATE TABLE public.public_control (
 id integer PRIMARY KEY CHECK(id=1), enabled boolean NOT NULL DEFAULT false,
 policy_digest bytea CHECK(octet_length(policy_digest)=32), last_clock timestamptz,
 incident text, active_campaign text REFERENCES public.public_campaign ON DELETE RESTRICT,
 CHECK(NOT enabled OR (policy_digest IS NOT NULL AND active_campaign IS NOT NULL AND incident
 IS NULL))
);
-- statement
CREATE TABLE public.public_day (
 campaign_id text REFERENCES public.public_campaign ON DELETE RESTRICT,
 utc_date date, limit_micro bigint NOT NULL DEFAULT 4000000 CHECK(limit_micro=4000000),
 available bigint NOT NULL DEFAULT 4000000 CHECK(available>=0),
 held bigint NOT NULL DEFAULT 0 CHECK(held>=0), settled bigint NOT NULL DEFAULT 0 CHECK(settled>=0),
 admitted_count integer NOT NULL DEFAULT 0 CHECK(admitted_count BETWEEN 0 AND 20),
 PRIMARY KEY(campaign_id,utc_date), CHECK(available+held+settled=limit_micro)
);
-- statement
CREATE TABLE public.public_client (
 campaign_id text REFERENCES public.public_campaign ON DELETE RESTRICT,
 bucket_hash bytea CHECK(octet_length(bucket_hash)=32), key_version text NOT NULL,
 created_at timestamptz NOT NULL, retention_until timestamptz NOT NULL,
 PRIMARY KEY(campaign_id,bucket_hash), CHECK(retention_until>=created_at)
);
-- statement
CREATE TABLE public.public_run (
 run_id bytea PRIMARY KEY CHECK(octet_length(run_id)=16), campaign_id text NOT NULL,
 utc_date date NOT NULL, bucket_hash bytea NOT NULL, admitted_at timestamptz NOT NULL,
 deadline timestamptz NOT NULL, read_expires timestamptz NOT NULL,
 state text NOT NULL CHECK(state IN ('ADMITTED','DISPATCH_STARTED','GOVERNANCE_PENDING',
 'UNKNOWN_OUTCOME','COMPLETED','FAILED_NOT_DISPATCHED','FAILED_PROVIDER','FAILED_TIMEOUT','FAILED_SAFETY')),
 owner_binding text UNIQUE, version bigint NOT NULL DEFAULT 1 CHECK(version>=1),
 read_hash bytea NOT NULL UNIQUE CHECK(octet_length(read_hash)=32),
 policy_digest bytea NOT NULL CHECK(octet_length(policy_digest)=32),
 payload_digest bytea NOT NULL CHECK(octet_length(payload_digest)=32),
 scenario_digest bytea NOT NULL CHECK(octet_length(scenario_digest)=32),
 FOREIGN KEY(campaign_id,utc_date) REFERENCES public.public_day ON DELETE RESTRICT,
 FOREIGN KEY(campaign_id,bucket_hash) REFERENCES public.public_client ON DELETE RESTRICT,
 UNIQUE(run_id,campaign_id,utc_date,bucket_hash),
 CHECK(deadline=admitted_at+interval '90 seconds'),
 CHECK(read_expires=admitted_at+interval '24 hours'),
 CHECK(utc_date=(admitted_at AT TIME ZONE 'UTC')::date)
);
-- statement
CREATE TABLE public.public_idempotency (
 campaign_id text, key_hash bytea CHECK(octet_length(key_hash)=32),
 bucket_hash bytea NOT NULL, payload_hash bytea NOT NULL CHECK(octet_length(payload_hash)=32),
 run_id bytea NOT NULL UNIQUE REFERENCES public.public_run ON DELETE RESTRICT,
 admitted_at timestamptz NOT NULL, replay_until timestamptz NOT NULL, retention_until
 timestamptz NOT NULL,
 PRIMARY KEY(campaign_id,key_hash),
 FOREIGN KEY(campaign_id,bucket_hash) REFERENCES public.public_client ON DELETE RESTRICT,
 CHECK(replay_until=admitted_at+interval '600 seconds'), CHECK(retention_until>=replay_until)
);
-- statement
CREATE TABLE public.public_rate_event (
 run_id bytea PRIMARY KEY, campaign_id text NOT NULL, utc_date date NOT NULL,
 bucket_hash bytea NOT NULL, admitted_at timestamptz NOT NULL,
 FOREIGN KEY(run_id,campaign_id,utc_date,bucket_hash)
 REFERENCES public.public_run(run_id,campaign_id,utc_date,bucket_hash) ON DELETE RESTRICT
);
-- statement
CREATE TABLE public.public_reservation (
 run_id bytea PRIMARY KEY REFERENCES public.public_run ON DELETE RESTRICT,
 campaign_id text NOT NULL, utc_date date NOT NULL,
 amount bigint NOT NULL DEFAULT 200000 CHECK(amount=200000),
 committed_max bigint NOT NULL DEFAULT 0 CHECK(committed_max BETWEEN 0 AND 200000),
 provisional bigint NOT NULL DEFAULT 0 CHECK(provisional>=0 AND provisional<=committed_max),
 settled_cost bigint CHECK(settled_cost BETWEEN 0 AND 200000 AND settled_cost<=committed_max),
 state text NOT NULL DEFAULT 'HELD' CHECK(state IN ('HELD','SETTLED','INCIDENT')),
 FOREIGN KEY(campaign_id,utc_date) REFERENCES public.public_day ON DELETE RESTRICT,
 CHECK((state='SETTLED')=(settled_cost IS NOT NULL))
);
-- statement
CREATE TABLE public.public_slot (
 slot_id integer PRIMARY KEY CHECK(slot_id IN (1,2)),
 run_id bytea UNIQUE REFERENCES public.public_run ON DELETE RESTRICT,
 generation bigint NOT NULL DEFAULT 1 CHECK(generation>=1),
 state text NOT NULL DEFAULT 'FREE' CHECK(state IN ('FREE','OCCUPIED','SUSPECT')),
 heartbeat_at timestamptz, expires_at timestamptz,
 CHECK((state='FREE')=(run_id IS NULL)),
 CHECK(state='FREE' OR (heartbeat_at IS NOT NULL AND expires_at=heartbeat_at+interval '15 seconds'))
);
-- statement
CREATE TABLE public.public_outbox (
 run_id bytea PRIMARY KEY REFERENCES public.public_run ON DELETE RESTRICT,
 state text NOT NULL DEFAULT 'PENDING' CHECK(state IN ('PENDING','BOUND','CLOSED')),
 generation bigint NOT NULL CHECK(generation>=1), owner_binding text UNIQUE,
 fenced_at timestamptz,
 CHECK(state<>'BOUND' OR owner_binding IS NOT NULL)
);
-- statement
CREATE TABLE public.public_dispatch (
 run_id bytea REFERENCES public.public_run ON DELETE RESTRICT,
 ordinal integer CHECK(ordinal IN (1,2)), generation bigint NOT NULL CHECK(generation>=1),
 start_marker_at timestamptz NOT NULL, max_cost bigint NOT NULL CHECK(max_cost>0 AND
 max_cost<=200000),
 state text NOT NULL CHECK(state IN ('STARTED','KNOWN_SUCCESS','KNOWN_FAILURE','UNKNOWN')),
 usage_evidence_digest bytea CHECK(octet_length(usage_evidence_digest)=32),
 provisional_cost bigint NOT NULL DEFAULT 0 CHECK(provisional_cost>=0 AND
 provisional_cost<=max_cost),
 PRIMARY KEY(run_id,ordinal)
);
-- statement
CREATE TABLE public.public_money_event (
 run_id bytea REFERENCES public.public_run ON DELETE RESTRICT,
 event_kind text CHECK(event_kind IN ('RESERVE','SETTLE')),
 amount bigint NOT NULL CHECK(amount=200000), cost bigint NOT NULL CHECK(cost BETWEEN 0 AND 200000),
 release bigint NOT NULL CHECK(release BETWEEN 0 AND 200000),
 campaign_id text NOT NULL, utc_date date NOT NULL,
 evidence_digest bytea NOT NULL CHECK(octet_length(evidence_digest)=32), created_at
 timestamptz NOT NULL,
 PRIMARY KEY(run_id,event_kind),
 FOREIGN KEY(campaign_id,utc_date) REFERENCES public.public_day ON DELETE RESTRICT,
 CHECK((event_kind='RESERVE' AND cost=0 AND release=0) OR (event_kind='SETTLE' AND
 cost+release=amount))
);
-- statement
CREATE TABLE public.public_observation (
 observation_id bytea PRIMARY KEY CHECK(octet_length(observation_id)=16),
 run_id bytea NOT NULL REFERENCES public.public_run ON DELETE RESTRICT, ordinal integer,
 source_identity bytea NOT NULL UNIQUE CHECK(octet_length(source_identity)=32),
 classification text NOT NULL CHECK(classification IN ('KNOWN_SUCCESS','KNOWN_FAILURE','UNKNOWN',
 'USAGE','ABOVE_BOUND','CLOSURE','LATE_USAGE')),
 evidence_digest bytea NOT NULL CHECK(octet_length(evidence_digest)=32),
 recorded_at timestamptz NOT NULL, cost_micro bigint CHECK(cost_micro>=0),
 FOREIGN KEY(run_id,ordinal) REFERENCES public.public_dispatch ON DELETE RESTRICT
);
-- statement
CREATE INDEX public_run_deadline ON public.public_run(state,deadline);
-- statement
CREATE INDEX public_run_read_expiry ON public.public_run(read_expires);
-- statement
CREATE INDEX public_key_retention ON public.public_idempotency(retention_until);
-- statement
CREATE INDEX public_client_retention ON public.public_client(retention_until);
-- statement
CREATE INDEX public_rate_hour ON public.public_rate_event(campaign_id,bucket_hash,admitted_at);
-- statement
CREATE INDEX public_rate_day ON public.public_rate_event(campaign_id,utc_date);
-- statement
CREATE INDEX public_outbox_pending ON public.public_outbox(state,run_id);
-- statement
INSERT INTO public.public_control(id) VALUES(1);
-- statement
INSERT INTO public.public_slot(slot_id) VALUES(1),(2);
-- statement
CREATE FUNCTION public_live_api.immutable() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN RAISE EXCEPTION 'PUBLIC_LIVE_APPEND_ONLY'; END $$;
-- statement
CREATE FUNCTION public_live_api.campaign_pins() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF (to_jsonb(NEW)-ARRAY['available','held','settled']) IS DISTINCT FROM
    (to_jsonb(OLD)-ARRAY['available','held','settled']) THEN
  RAISE EXCEPTION 'PUBLIC_CAMPAIGN_PINS_IMMUTABLE';
 END IF;
 RETURN NEW;
END $$;
-- statement
CREATE TRIGGER campaign_pins BEFORE UPDATE ON public.public_campaign
FOR EACH ROW EXECUTE FUNCTION public_live_api.campaign_pins();
-- statement
CREATE TRIGGER fixed_slots BEFORE DELETE ON public.public_slot
FOR EACH ROW EXECUTE FUNCTION public_live_api.immutable();
-- statement
CREATE TRIGGER fixed_slots_truncate BEFORE TRUNCATE ON public.public_slot
FOR EACH STATEMENT EXECUTE FUNCTION public_live_api.immutable();
-- statement
CREATE FUNCTION public_live_api.clock_lock() RETURNS timestamptz
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE prior timestamptz; now_at timestamptz;
BEGIN
 SELECT last_clock INTO prior FROM public.public_control WHERE id=1 FOR UPDATE;
 IF NOT FOUND THEN RAISE EXCEPTION 'PUBLIC_CONTROL_MISSING'; END IF;
 now_at:=clock_timestamp();
 IF prior IS NOT NULL AND now_at<prior THEN
   UPDATE public.public_control SET enabled=false,incident='CLOCK_REGRESSION' WHERE id=1;
   RETURN prior;
 END IF;
 UPDATE public.public_control SET last_clock=now_at WHERE id=1;
 RETURN now_at;
END $$;
-- statement
CREATE FUNCTION public_live_api.read_key(c text,k bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE result jsonb;
BEGIN
 PERFORM public_live_api.clock_lock();
 SELECT to_jsonb(i) INTO result FROM public.public_idempotency i
 WHERE campaign_id=c AND key_hash=k FOR UPDATE;
 RETURN result;
END $$;
-- statement
CREATE FUNCTION public_live_api.lock_context(c text,days date[],bucket bytea) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE d date; now_at timestamptz; campaign public.public_campaign;
BEGIN
 now_at:=public_live_api.clock_lock();
 SELECT * INTO STRICT campaign FROM public.public_campaign WHERE campaign_id=c FOR UPDATE;
 FOR d IN SELECT DISTINCT unnest(days) ORDER BY 1 LOOP
   INSERT INTO public.public_day(campaign_id,utc_date) VALUES(c,d) ON CONFLICT DO NOTHING;
   PERFORM 1 FROM public.public_day WHERE campaign_id=c AND utc_date=d FOR UPDATE;
 END LOOP;
 INSERT INTO public.public_client VALUES(c,bucket,campaign.hmac_version,now_at,
 campaign.ends_at+interval '30 days') ON CONFLICT DO NOTHING;
 PERFORM 1 FROM public.public_client WHERE campaign_id=c AND bucket_hash=bucket FOR UPDATE;
 PERFORM 1 FROM public.public_slot ORDER BY slot_id FOR UPDATE;
 IF (SELECT count(*) FROM public.public_slot)<>2 THEN RAISE EXCEPTION 'SLOT_DOMAIN_INVALID'; END IF;
END $$;
-- statement
CREATE FUNCTION public_live_api.persist_run(p jsonb) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE r bytea:=decode(p->>'run_id','hex'); b bytea:=decode(p->>'bucket_hash','hex');
 c text:=p->>'campaign_id'; k bytea:=decode(p->>'key_hash','hex');
 now_at timestamptz; d date; campaign public.public_campaign; s public.public_slot;
BEGIN
 now_at:=public_live_api.clock_lock();
 PERFORM public_live_api.read_key(c,k);
 d:=(now_at AT TIME ZONE 'UTC')::date;
 PERFORM public_live_api.lock_context(c,ARRAY[d],b);
 SELECT * INTO STRICT campaign FROM public.public_campaign WHERE campaign_id=c;
 SELECT * INTO STRICT s FROM public.public_slot WHERE slot_id=(p->>'slot_id')::integer;
 IF NOT EXISTS(SELECT 1 FROM public.public_control WHERE enabled AND incident IS NULL
 AND active_campaign=c AND policy_digest=campaign.policy_digest) OR now_at<campaign.starts_at
 OR now_at>=campaign.ends_at THEN RAISE EXCEPTION 'PUBLIC_LIVE_DISABLED'; END IF;
 IF s.state<>'FREE' THEN RAISE EXCEPTION 'SLOT_NOT_FREE'; END IF;
 INSERT INTO public.public_run VALUES(r,c,d,b,now_at,now_at+interval '90 seconds',
 now_at+interval '24 hours','ADMITTED',NULL,1,decode(p->>'read_hash','hex'),
 campaign.policy_digest,decode(p->>'payload_digest','hex'),campaign.content_digest);
 INSERT INTO public.public_idempotency VALUES(c,k,b,decode(p->>'payload_digest','hex'),r,
 now_at,now_at+interval '600 seconds',campaign.ends_at+interval '30 days');
 INSERT INTO public.public_rate_event VALUES(r,c,d,b,now_at);
 INSERT INTO public.public_reservation(run_id,campaign_id,utc_date) VALUES(r,c,d);
 INSERT INTO public.public_money_event VALUES(r,'RESERVE',200000,0,0,c,d,
 decode(p->>'payload_digest','hex'),now_at);
 UPDATE public.public_campaign SET available=available-200000,held=held+200000 WHERE campaign_id=c;
 UPDATE public.public_day SET available=available-200000,held=held+200000,
 admitted_count=admitted_count+1 WHERE campaign_id=c AND utc_date=d;
 UPDATE public.public_slot SET state='OCCUPIED',run_id=r,heartbeat_at=now_at,
 expires_at=now_at+interval '15 seconds' WHERE slot_id=s.slot_id;
 INSERT INTO public.public_outbox(run_id,generation) VALUES(r,s.generation);
END $$;
-- statement
CREATE FUNCTION public_live_api.lock_run(r bytea) RETURNS public.public_run
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE v public.public_run;
BEGIN
 PERFORM public_live_api.clock_lock();
 SELECT * INTO STRICT v FROM public.public_run WHERE run_id=r;
 PERFORM 1 FROM public.public_campaign WHERE campaign_id=v.campaign_id FOR UPDATE;
 PERFORM 1 FROM public.public_day WHERE campaign_id=v.campaign_id AND utc_date=v.utc_date FOR
 UPDATE;
 PERFORM 1 FROM public.public_client WHERE campaign_id=v.campaign_id AND
 bucket_hash=v.bucket_hash FOR UPDATE;
 PERFORM 1 FROM public.public_slot ORDER BY slot_id FOR UPDATE;
 SELECT * INTO STRICT v FROM public.public_run WHERE run_id=r FOR UPDATE;
 PERFORM 1 FROM public.public_dispatch WHERE run_id=r ORDER BY ordinal FOR UPDATE;
 RETURN v;
END $$;
-- statement
CREATE FUNCTION public_live_api.slot_update(r bytea,g bigint,suspect boolean) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE now_at timestamptz;
BEGIN
 PERFORM public_live_api.lock_run(r); now_at:=public_live_api.clock_lock();
 IF suspect THEN
  UPDATE public.public_slot SET state='SUSPECT' WHERE run_id=r AND generation=g AND state<>'FREE';
 ELSE
  UPDATE public.public_slot SET heartbeat_at=now_at,expires_at=now_at+interval '15 seconds'
  WHERE run_id=r AND generation=g AND state='OCCUPIED' AND expires_at>now_at;
 END IF;
 IF NOT FOUND THEN RAISE EXCEPTION 'STALE_OR_QUARANTINED_SLOT'; END IF;
END $$;
-- statement
CREATE FUNCTION public_live_api.mark_dispatch(r bytea,g bigint,n integer,bound bigint) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE v public.public_run; now_at timestamptz;
BEGIN
 v:=public_live_api.lock_run(r);now_at:=public_live_api.clock_lock();
 IF now_at>=v.deadline OR NOT EXISTS(SELECT 1 FROM public.public_control WHERE enabled AND
 incident IS NULL)
 OR NOT EXISTS(SELECT 1 FROM public.public_slot WHERE run_id=r AND generation=g AND
 state='OCCUPIED' AND expires_at>now_at)
 OR NOT EXISTS(SELECT 1 FROM public.public_outbox WHERE run_id=r AND generation=g AND state='BOUND')
 THEN RAISE EXCEPTION 'DISPATCH_CLOSED'; END IF;
 IF n=2 AND NOT EXISTS(SELECT 1 FROM public.public_dispatch WHERE run_id=r AND ordinal=1 AND
 state='KNOWN_FAILURE')
 THEN RAISE EXCEPTION 'RETRY_NOT_KNOWN_FAILURE'; END IF;
 INSERT INTO public.public_dispatch VALUES(r,n,g,now_at,bound,'STARTED',NULL,0);
 UPDATE public.public_reservation SET committed_max=committed_max+bound WHERE run_id=r AND
 state='HELD';
 IF NOT FOUND THEN RAISE EXCEPTION 'RESERVATION_NOT_HELD'; END IF;
 UPDATE public.public_run SET state='DISPATCH_STARTED',version=version+1 WHERE run_id=r;
END $$;
-- statement
CREATE FUNCTION public_live_api.observe(p jsonb) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE r bytea:=decode(p->>'run_id','hex'); now_at timestamptz;
BEGIN
 PERFORM public_live_api.lock_run(r);now_at:=public_live_api.clock_lock();
 IF p->>'classification'='CLOSURE' THEN
  RAISE EXCEPTION 'CLOSURE_REQUIRES_SEPARATE_ADMITTED_AUTHORITY';
 END IF;
 INSERT INTO public.public_observation VALUES(decode(p->>'observation_id','hex'),r,
 (p->>'ordinal')::integer,decode(p->>'source_identity','hex'),p->>'classification',
 decode(p->>'evidence_digest','hex'),now_at,(p->>'cost_micro')::bigint);
 IF p->>'classification'='ABOVE_BOUND' THEN
  UPDATE public.public_control SET enabled=false,incident='ABOVE_BOUND_USAGE' WHERE id=1;
  UPDATE public.public_reservation SET state='INCIDENT' WHERE run_id=r AND state='HELD';
  UPDATE public.public_slot SET state='SUSPECT' WHERE run_id=r;
 END IF;
END $$;
-- statement
CREATE FUNCTION public_live_api.read_outbox(r bytea) RETURNS jsonb
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE result jsonb;
BEGIN
 PERFORM public_live_api.lock_run(r);
 SELECT to_jsonb(o) INTO result FROM public.public_outbox o WHERE run_id=r;
 RETURN result;
END $$;
-- statement
CREATE FUNCTION public_live_api.fence_run(r bytea,g bigint) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE now_at timestamptz;
BEGIN
 PERFORM public_live_api.lock_run(r);now_at:=public_live_api.clock_lock();
 UPDATE public.public_outbox SET state='CLOSED',generation=generation+1,fenced_at=now_at
 WHERE run_id=r AND generation=g AND state<>'CLOSED';
 IF NOT FOUND THEN RAISE EXCEPTION 'FENCE_GENERATION_CONFLICT'; END IF;
 UPDATE public.public_slot SET state='SUSPECT' WHERE run_id=r AND generation=g;
 IF NOT FOUND THEN RAISE EXCEPTION 'FENCE_SLOT_CONFLICT'; END IF;
END $$;
-- statement
CREATE FUNCTION public_live_api.settle(r bytea,cost_value bigint,proof bytea) RETURNS boolean
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE v public.public_run; res public.public_reservation; prior public.public_money_event;
 now_at timestamptz;
BEGIN
 v:=public_live_api.lock_run(r);now_at:=public_live_api.clock_lock();
 SELECT * INTO prior FROM public.public_money_event WHERE run_id=r AND event_kind='SETTLE';
 IF FOUND THEN
  IF prior.cost<>cost_value OR prior.evidence_digest<>proof THEN RAISE EXCEPTION
 'SETTLEMENT_CONFLICT'; END IF;
  RETURN false;
 END IF;
 SELECT * INTO STRICT res FROM public.public_reservation WHERE run_id=r FOR UPDATE;
 IF res.state<>'HELD' OR cost_value<0 OR cost_value>res.committed_max OR NOT EXISTS(
 SELECT 1 FROM public.public_observation o JOIN public.public_outbox b USING(run_id)
 WHERE o.run_id=r AND o.classification='CLOSURE' AND o.evidence_digest=proof
 AND b.state='CLOSED' AND b.fenced_at IS NOT NULL AND o.recorded_at>=b.fenced_at
 AND o.cost_micro=cost_value)
 THEN RAISE EXCEPTION 'CLOSURE_OR_CONSERVATIVE_COST_REQUIRED'; END IF;
 INSERT INTO public.public_money_event VALUES(r,'SETTLE',200000,cost_value,200000-cost_value,
 v.campaign_id,v.utc_date,proof,now_at);
 UPDATE public.public_campaign SET held=held-200000,settled=settled+cost_value,
 available=available+200000-cost_value WHERE campaign_id=v.campaign_id;
 UPDATE public.public_day SET held=held-200000,settled=settled+cost_value,
 available=available+200000-cost_value WHERE campaign_id=v.campaign_id AND utc_date=v.utc_date;
 UPDATE public.public_reservation SET settled_cost=cost_value,state='SETTLED' WHERE run_id=r;
 UPDATE public.public_outbox SET state='CLOSED',generation=generation+1 WHERE run_id=r;
 UPDATE public.public_slot SET run_id=NULL,state='FREE',generation=generation+1,
 heartbeat_at=NULL,expires_at=NULL WHERE run_id=r;
 RETURN true;
END $$;
-- statement
CREATE FUNCTION public_live_api.bind_owner(r bytea,g bigint,owner_id text) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
BEGIN
 PERFORM public_live_api.lock_run(r);
 IF NOT EXISTS(SELECT 1 FROM public.work_runs WHERE work_run_id=owner_id
 AND runtime_mode='PUBLIC_BOUNDED_LIVE') THEN RAISE EXCEPTION
 'PUBLIC_OWNER_BINDING_REQUIRED'; END IF;
 UPDATE public.public_outbox SET owner_binding=owner_id,state='BOUND'
 WHERE run_id=r AND generation=g AND state='PENDING';
 IF NOT FOUND THEN RAISE EXCEPTION 'OUTBOX_BINDING_CONFLICT'; END IF;
 UPDATE public.public_run SET owner_binding=owner_id,version=version+1 WHERE run_id=r;
END $$;
-- statement
CREATE FUNCTION public_live_api.record_outcome(r bytea,n integer,kind text,cost_value bigint,
 proof bytea,identity bytea,observation bytea) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE marker public.public_dispatch;
BEGIN
 PERFORM public_live_api.lock_run(r);
 SELECT * INTO STRICT marker FROM public.public_dispatch WHERE run_id=r AND ordinal=n;
 IF kind NOT IN ('KNOWN_SUCCESS','KNOWN_FAILURE','UNKNOWN') OR marker.state<>'STARTED'
 THEN RAISE EXCEPTION 'DISPATCH_OUTCOME_CONFLICT'; END IF;
 IF cost_value<0 OR cost_value>marker.max_cost OR (kind='UNKNOWN' AND cost_value<>marker.max_cost)
 THEN RAISE EXCEPTION 'DISPATCH_COST_INVALID'; END IF;
 INSERT INTO public.public_observation VALUES(observation,r,n,identity,kind,proof,
 public_live_api.clock_lock(),cost_value);
 UPDATE public.public_dispatch SET state=kind,provisional_cost=cost_value,
 usage_evidence_digest=proof WHERE run_id=r AND ordinal=n;
END $$;
-- statement
CREATE FUNCTION public_live_api.admit_closure(r bytea,g bigint,cost_value bigint,
 proof bytea,identity bytea,observation bytea) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog AS $$
DECLARE expected_cost bigint;
BEGIN
 PERFORM public_live_api.lock_run(r);
 IF NOT EXISTS(SELECT 1 FROM public.public_outbox WHERE run_id=r AND generation=g
 AND state='CLOSED' AND fenced_at IS NOT NULL) THEN RAISE EXCEPTION 'RUN_NOT_FENCED'; END IF;
 SELECT coalesce(sum(CASE WHEN state IN ('KNOWN_SUCCESS','KNOWN_FAILURE')
 THEN provisional_cost ELSE max_cost END),0) INTO expected_cost
 FROM public.public_dispatch WHERE run_id=r;
 IF cost_value<>expected_cost THEN RAISE EXCEPTION 'CLOSURE_COST_CONFLICT'; END IF;
 INSERT INTO public.public_observation VALUES(observation,r,NULL,identity,'CLOSURE',proof,
 public_live_api.clock_lock(),cost_value);
END $$;
-- statement
CREATE VIEW public_live_api.safe_status AS
 SELECT encode(run_id,'hex') AS run_id,state,admitted_at,deadline FROM public.public_run;
"""


def upgrade():
    for statement in DDL.split("-- statement"):
        op.execute(statement)
    for table in (
        "public_money_event",
        "public_observation",
        "public_rate_event",
        "public_idempotency",
    ):
        op.execute(
            f"CREATE TRIGGER immutable_rows BEFORE UPDATE OR DELETE ON public.{table} "
            "FOR EACH ROW EXECUTE FUNCTION public_live_api.immutable()"
        )
        op.execute(
            f"CREATE TRIGGER immutable_truncate BEFORE TRUNCATE ON public.{table} "
            "FOR EACH STATEMENT EXECUTE FUNCTION public_live_api.immutable()"
        )
    op.execute("""DO $$ BEGIN
      IF NOT EXISTS(SELECT 1 FROM pg_roles WHERE rolname='aiscc_public_live_runtime') THEN
        CREATE ROLE aiscc_public_live_runtime NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
      END IF;
      IF EXISTS(SELECT 1 FROM pg_roles WHERE rolname='aiscc_public_live_runtime'
      AND (rolsuper OR rolcreatedb OR rolcreaterole OR rolcanlogin OR rolinherit)) THEN
        RAISE EXCEPTION 'PUBLIC_RUNTIME_ROLE_UNSAFE';
      END IF;
    END $$""")
    op.execute("REVOKE ALL ON SCHEMA public_live_api FROM PUBLIC")
    op.execute("REVOKE ALL ON ALL FUNCTIONS IN SCHEMA public_live_api FROM PUBLIC")
    op.execute("GRANT USAGE ON SCHEMA public_live_api TO aiscc_public_live_runtime")
    op.execute(
        "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public_live_api TO aiscc_public_live_runtime"
    )
    op.execute("GRANT SELECT ON public_live_api.safe_status TO aiscc_public_live_runtime")
    # Only a separately configured trusted reconciler may admit execution/closure
    # facts. These are persistence primitives, not verification of external truth.
    op.execute("""DO $$ BEGIN
      IF NOT EXISTS(SELECT 1 FROM pg_roles WHERE rolname='aiscc_public_live_reconciler') THEN
        CREATE ROLE aiscc_public_live_reconciler NOLOGIN NOSUPERUSER
        NOCREATEDB NOCREATEROLE NOINHERIT;
      END IF;
      IF EXISTS(SELECT 1 FROM pg_roles WHERE rolname='aiscc_public_live_reconciler'
      AND (rolsuper OR rolcreatedb OR rolcreaterole OR rolcanlogin OR rolinherit)) THEN
        RAISE EXCEPTION 'PUBLIC_RECONCILER_ROLE_UNSAFE';
      END IF;
    END $$""")
    op.execute("GRANT USAGE ON SCHEMA public_live_api TO aiscc_public_live_reconciler")
    op.execute(
        "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public_live_api TO aiscc_public_live_reconciler"
    )
    for signature in (
        "bind_owner(bytea,bigint,text)",
        "record_outcome(bytea,integer,text,bigint,bytea,bytea,bytea)",
        "admit_closure(bytea,bigint,bigint,bytea,bytea,bytea)",
    ):
        op.execute(
            f"REVOKE EXECUTE ON FUNCTION public_live_api.{signature} FROM aiscc_public_live_runtime"
        )
    for table in TABLES:
        op.execute(f"REVOKE ALL ON public.{table} FROM PUBLIC, aiscc_public_live_runtime")


def downgrade():
    for table in TABLES:
        if table not in ("public_control", "public_slot") and op.get_bind().scalar(
            sa.text(f"SELECT EXISTS(SELECT 1 FROM public.{table})")
        ):
            raise RuntimeError("PUBLIC_LIVE_NONEMPTY_DOWNGRADE_FORBIDDEN")
    if op.get_bind().scalar(
        sa.text(
            "SELECT EXISTS(SELECT 1 FROM public.public_control "
            "WHERE enabled OR incident IS NOT NULL)"
        )
    ):
        raise RuntimeError("PUBLIC_LIVE_UNSAFE_DOWNGRADE_FORBIDDEN")
    op.execute("DROP SCHEMA public_live_api CASCADE")
    # All public tables are proven empty apart from disabled control/free slots.
    for table in (
        "public_observation",
        "public_money_event",
        "public_dispatch",
        "public_outbox",
        "public_slot",
        "public_reservation",
        "public_rate_event",
        "public_idempotency",
        "public_run",
        "public_client",
        "public_day",
        "public_control",
        "public_campaign",
    ):
        op.drop_table(table)
    # Shared NOLOGIN role may serve another isolated DB; never drop it here.
