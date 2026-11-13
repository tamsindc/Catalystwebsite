// Public site settings. Both Supabase values are designed to be public (the key is the
// project's "publishable" or "anon" key). The signups table only accepts new rows, so
// visitors cannot read anyone else's details. See supabase/schema.sql.
window.FP_CONFIG = {
  supabaseUrl: '',   // e.g. https://abcd1234.supabase.co
  supabaseKey: '',   // the publishable / anon key, never the service_role key
};
