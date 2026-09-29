-- Smart Lost & Found — Supabase schema
-- Run this once in: Supabase Dashboard → SQL Editor → New query → Run

-- ---------- USERS ----------
create table if not exists public.users (
    id          bigint generated always as identity primary key,
    username    text unique not null,
    password    text not null,              -- "salt:pbkdf2_hash" (hashed in the app)
    created_at  timestamptz not null default now()
);

-- ---------- REPORTS ----------
create table if not exists public.reports (
    id             bigint generated always as identity primary key,
    report_type    text not null check (report_type in ('Lost', 'Found')),
    item_name      text not null,
    category       text,
    description    text,
    location       text,
    date_reported  timestamptz not null default now(),
    image_path     text,                    -- public URL in Supabase Storage
    contact        text,
    status         text not null default 'Active',
    reported_by    text,                    -- username of the reporter
    created_at     timestamptz not null default now()
);

create index if not exists reports_type_idx on public.reports (report_type);

-- ---------- SECURITY ----------
-- RLS on with no policies = nobody can read/write through the public
-- (anon/publishable) key. The Streamlit server uses the SECRET key,
-- which bypasses RLS, so the app works and the tables stay locked down.
alter table public.users   enable row level security;
alter table public.reports enable row level security;

-- ---------- IMAGE STORAGE ----------
-- Public bucket so st.image() can load photos straight from the URL.
insert into storage.buckets (id, name, public)
values ('item-images', 'item-images', true)
on conflict (id) do nothing;
