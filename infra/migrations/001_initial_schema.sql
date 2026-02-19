-- Learn Plattform: Initial Schema
-- Run in Supabase SQL Editor

-- Users profile table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    name TEXT DEFAULT '',
    yearly_goal TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own profile" ON public.users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.users FOR UPDATE USING (auth.uid() = id);

-- Auto-create user profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.users (id, email, name)
    VALUES (NEW.id, NEW.email, NEW.raw_user_meta_data->>'full_name');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Learning Paths
CREATE TABLE IF NOT EXISTS public.learning_paths (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed')),
    created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.learning_paths ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage own paths" ON public.learning_paths
    FOR ALL USING (auth.uid() = user_id);

-- Epubs
CREATE TABLE IF NOT EXISTS public.epubs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    learning_path_id UUID NOT NULL REFERENCES public.learning_paths(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    total_chapters INTEGER DEFAULT 1,
    current_chapter INTEGER DEFAULT 0,
    progress_percent NUMERIC(5,2) DEFAULT 0,
    uploaded_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.epubs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage own epubs" ON public.epubs
    FOR ALL USING (auth.uid() = user_id);

-- Quizzes
CREATE TABLE IF NOT EXISTS public.quizzes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    epub_id UUID NOT NULL REFERENCES public.epubs(id) ON DELETE CASCADE,
    chapter INTEGER NOT NULL,
    questions JSONB NOT NULL DEFAULT '[]',
    answers JSONB,
    score NUMERIC(5,2),
    taken_at TIMESTAMPTZ
);

ALTER TABLE public.quizzes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage own quizzes" ON public.quizzes
    FOR ALL USING (
        EXISTS (SELECT 1 FROM public.epubs WHERE epubs.id = quizzes.epub_id AND epubs.user_id = auth.uid())
    );

-- News Sources (intermediate table for worker pipeline)
CREATE TABLE IF NOT EXISTS public.news_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type TEXT NOT NULL CHECK (source_type IN ('gmail', 'rss', 'scraping')),
    title TEXT,
    content TEXT,
    url TEXT,
    links JSONB DEFAULT '[]',
    raw_data JSONB DEFAULT '{}',
    published_at TIMESTAMPTZ,
    fetched_at TIMESTAMPTZ DEFAULT now()
);

-- News Pages (generated daily content)
CREATE TABLE IF NOT EXISTS public.news_pages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL UNIQUE,
    content TEXT NOT NULL,
    sources JSONB DEFAULT '[]',
    generated_at TIMESTAMPTZ DEFAULT now()
);

-- Videos
CREATE TABLE IF NOT EXISTS public.videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    description TEXT DEFAULT '',
    published_at TIMESTAMPTZ,
    discovered_at TIMESTAMPTZ DEFAULT now()
);

-- Critiques
CREATE TABLE IF NOT EXISTS public.critiques (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    period TEXT DEFAULT 'weekly',
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.critiques ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own critiques" ON public.critiques
    FOR ALL USING (auth.uid() = user_id);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_learning_paths_user ON public.learning_paths(user_id);
CREATE INDEX IF NOT EXISTS idx_epubs_user ON public.epubs(user_id);
CREATE INDEX IF NOT EXISTS idx_epubs_path ON public.epubs(learning_path_id);
CREATE INDEX IF NOT EXISTS idx_quizzes_epub ON public.quizzes(epub_id);
CREATE INDEX IF NOT EXISTS idx_news_sources_fetched ON public.news_sources(fetched_at);
CREATE INDEX IF NOT EXISTS idx_news_pages_date ON public.news_pages(date);
CREATE INDEX IF NOT EXISTS idx_videos_source ON public.videos(source);
CREATE INDEX IF NOT EXISTS idx_videos_discovered ON public.videos(discovered_at);
CREATE INDEX IF NOT EXISTS idx_critiques_user ON public.critiques(user_id);

-- Storage bucket for epubs
INSERT INTO storage.buckets (id, name, public) VALUES ('epubs', 'epubs', false)
ON CONFLICT DO NOTHING;

CREATE POLICY "Users can upload own epubs" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'epubs' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Users can read own epubs" ON storage.objects
    FOR SELECT USING (bucket_id = 'epubs' AND auth.uid()::text = (storage.foldername(name))[1]);
