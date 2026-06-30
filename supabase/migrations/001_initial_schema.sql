-- School Timeline: initial schema

CREATE TABLE grades (
  id          uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  grade_key   text UNIQUE NOT NULL,
  title       text NOT NULL,
  subtitle    text,
  school_year text NOT NULL
);

CREATE TABLE months (
  id          uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  grade_id    uuid REFERENCES grades(id) ON DELETE CASCADE,
  month_title text NOT NULL,
  month_order int  NOT NULL,
  UNIQUE(grade_id, month_order)
);

CREATE TABLE timeline_items (
  id          uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  month_id    uuid REFERENCES months(id) ON DELETE CASCADE,
  type        text NOT NULL CHECK (type IN ('lesson', 'assignment', 'test')),
  title       text NOT NULL,
  date_text   text NOT NULL,
  date_actual date,
  description text,
  details     text,
  icon        text,
  style       text,
  item_order  int  NOT NULL DEFAULT 0,
  created_at  timestamptz DEFAULT now()
);

CREATE TABLE grade_editors (
  grade_id   uuid REFERENCES grades(id) ON DELETE CASCADE,
  user_email text NOT NULL,
  PRIMARY KEY (grade_id, user_email)
);

-- RLS: public read on grades/months/items; service role handles all writes
ALTER TABLE grades         ENABLE ROW LEVEL SECURITY;
ALTER TABLE months         ENABLE ROW LEVEL SECURITY;
ALTER TABLE timeline_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE grade_editors  ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read" ON grades         FOR SELECT USING (true);
CREATE POLICY "public read" ON months         FOR SELECT USING (true);
CREATE POLICY "public read" ON timeline_items FOR SELECT USING (true);
-- grade_editors has no public policy → anon cannot read it; service role bypasses RLS
