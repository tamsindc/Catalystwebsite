-- fishpond sign-ups. Run once in the Supabase SQL editor (or via the Supabase connector).
create table if not exists public.signups (
  id         bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  email      text not null check (char_length(email) between 5 and 254 and email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
  list       text not null check (list in ('waitlist','early_access','creator','cohort','hiring','track')),
  name       text check (char_length(name) <= 120),
  org        text check (char_length(org) <= 160),
  role       text check (char_length(role) <= 160),
  link       text check (char_length(link) <= 500),
  note       text check (char_length(note) <= 1000),
  page       text check (char_length(page) <= 200),
  unique (email, list)
);

-- Visitors may add themselves, and nothing else: no reading, editing or deleting.
alter table public.signups enable row level security;
drop policy if exists "anyone can sign up" on public.signups;
create policy "anyone can sign up" on public.signups for insert to anon, authenticated with check (true);
revoke all on public.signups from anon, authenticated;
grant insert (email, list, name, org, role, link, note, page) on public.signups to anon, authenticated;
