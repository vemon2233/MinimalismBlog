import React, { useState, useEffect, useCallback } from 'react';
import { BlogPost, ViewState } from './types';
import { generateBlogContent, checkApiKey } from './services/geminiService';
import { Button } from './components/Button';
import { Tag } from './components/Tag';
import { Calendar, Edit3, ArrowLeft, Plus, Sparkles, X, Save } from 'lucide-react';

// --- Sub-components defined here for simplicity in file structure, 
// usually would be split but keeping them close for the "handful of files" requirement 
// while adhering to clean component separation rules.

// ---------------------------------------------------------------------------
// Component: Editor
// ---------------------------------------------------------------------------
interface EditorProps {
  initialPost?: BlogPost;
  onSave: (post: BlogPost) => void;
  onCancel: () => void;
}

const Editor: React.FC<EditorProps> = ({ initialPost, onSave, onCancel }) => {
  const [title, setTitle] = useState(initialPost?.title || '');
  const [content, setContent] = useState(initialPost?.content || '');
  const [tags, setTags] = useState<string>(initialPost?.tags.join(', ') || '');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAIHelp = async () => {
    if (!checkApiKey()) {
      setError("API Key not found in environment variables.");
      return;
    }
    if (!title.trim()) {
      setError("Please provide at least a title for the AI to work with.");
      return;
    }

    setIsGenerating(true);
    setError(null);
    try {
      const result = await generateBlogContent(title, content);
      setContent(result.content);
      // Append suggested tags to existing ones
      const currentTags = tags.split(',').map(t => t.trim()).filter(Boolean);
      const newTags = Array.from(new Set([...currentTags, ...result.tags]));
      setTags(newTags.join(', '));
    } catch (e) {
      setError("Failed to generate content. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSave = () => {
    if (!title.trim() || !content.trim()) {
      setError("Title and Content are required.");
      return;
    }

    const newPost: BlogPost = {
      id: initialPost?.id || crypto.randomUUID(),
      title,
      content,
      excerpt: content.slice(0, 150).replace(/[#*`]/g, '') + '...',
      tags: tags.split(',').map(t => t.trim()).filter(Boolean),
      createdAt: initialPost?.createdAt || Date.now(),
      updatedAt: Date.now(),
    };
    onSave(newPost);
  };

  return (
    <div className="max-w-3xl mx-auto animate-fade-in">
      <div className="mb-8 flex items-center justify-between">
        <h2 className="text-2xl font-serif font-bold text-stone-800">
          {initialPost ? 'Edit Article' : 'New Article'}
        </h2>
        <Button variant="ghost" onClick={onCancel}><X size={20} /></Button>
      </div>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-stone-500 mb-2">Title</label>
          <input
            type="text"
            className="w-full text-3xl font-serif font-bold bg-transparent border-b border-stone-300 focus:border-stone-800 outline-none pb-2 placeholder-stone-300 transition-colors"
            placeholder="Enter a compelling title..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="block text-sm font-medium text-stone-500">Content (Markdown supported)</label>
            <Button 
              type="button" 
              onClick={handleAIHelp} 
              disabled={isGenerating}
              variant="secondary"
              className="text-xs py-1"
            >
              <Sparkles size={14} className={isGenerating ? "animate-pulse" : ""} />
              {isGenerating ? 'Drafting...' : 'AI Draft'}
            </Button>
          </div>
          <textarea
            className="w-full h-96 p-4 rounded-lg bg-white border border-stone-200 focus:border-stone-400 outline-none resize-none font-mono text-sm leading-relaxed shadow-sm"
            placeholder="Write your thoughts here..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-stone-500 mb-2">Tags (comma separated)</label>
          <input
            type="text"
            className="w-full p-3 rounded-lg bg-white border border-stone-200 focus:border-stone-400 outline-none font-sans text-sm shadow-sm"
            placeholder="minimalism, tech, life"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
          />
        </div>

        {error && (
          <div className="p-3 bg-red-50 text-red-600 text-sm rounded-md border border-red-100">
            {error}
          </div>
        )}

        <div className="flex gap-4 pt-4 border-t border-stone-200">
          <Button onClick={handleSave} className="flex-1">
            <Save size={18} /> Save Article
          </Button>
          <Button variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        </div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Component: PostList
// ---------------------------------------------------------------------------
interface PostListProps {
  posts: BlogPost[];
  onSelect: (id: string) => void;
  selectedTag?: string;
  onTagClick: (tag: string) => void;
  onClearTag: () => void;
}

const PostList: React.FC<PostListProps> = ({ posts, onSelect, selectedTag, onTagClick, onClearTag }) => {
  const filteredPosts = selectedTag 
    ? posts.filter(p => p.tags.includes(selectedTag))
    : posts;

  if (filteredPosts.length === 0) {
    return (
      <div className="text-center py-20">
        <p className="text-stone-400 font-serif italic text-lg">No stories found.</p>
        {selectedTag && (
          <Button variant="ghost" onClick={onClearTag} className="mt-4">
            Clear filter
          </Button>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-12 max-w-3xl mx-auto">
      {selectedTag && (
        <div className="flex items-center gap-2 mb-8">
          <span className="text-stone-500 text-sm">Filtering by:</span>
          <Tag label={selectedTag} isActive onClick={onClearTag} />
          <button onClick={onClearTag} className="text-stone-400 hover:text-stone-600 ml-2">
            <X size={14} />
          </button>
        </div>
      )}

      {filteredPosts.map(post => (
        <article key={post.id} className="group cursor-pointer" onClick={() => onSelect(post.id)}>
          <div className="flex items-center gap-3 text-xs text-stone-400 mb-2 font-medium uppercase tracking-wider">
            <Calendar size={12} />
            {new Date(post.createdAt).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}
          </div>
          <h2 className="text-2xl font-serif font-bold text-stone-800 mb-3 group-hover:text-stone-600 transition-colors">
            {post.title}
          </h2>
          <p className="text-stone-600 leading-relaxed mb-4 font-serif">
            {post.excerpt}
          </p>
          <div className="flex gap-2 flex-wrap">
            {post.tags.map(tag => (
              <span 
                key={tag} 
                className="text-xs text-stone-400 hover:text-stone-600 z-10"
                onClick={(e) => {
                  e.stopPropagation();
                  onTagClick(tag);
                }}
              >
                #{tag}
              </span>
            ))}
          </div>
        </article>
      ))}
    </div>
  );
};

// ---------------------------------------------------------------------------
// Component: PostDetail
// ---------------------------------------------------------------------------
interface PostDetailProps {
  post: BlogPost;
  onBack: () => void;
  onEdit: () => void;
  onTagClick: (tag: string) => void;
}

const PostDetail: React.FC<PostDetailProps> = ({ post, onBack, onEdit, onTagClick }) => {
  return (
    <div className="max-w-3xl mx-auto animate-fade-in">
      <Button variant="ghost" onClick={onBack} className="mb-8 pl-0 hover:bg-transparent hover:text-stone-600">
        <ArrowLeft size={18} /> Back to list
      </Button>

      <article>
        <header className="mb-10 text-center">
          <div className="flex justify-center gap-4 text-xs text-stone-400 mb-4 font-medium uppercase tracking-wider">
             <span>{new Date(post.createdAt).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</span>
             <span>•</span>
             <span>{Math.ceil(post.content.split(' ').length / 200)} min read</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-serif font-bold text-stone-900 mb-6 leading-tight">
            {post.title}
          </h1>
          <div className="flex justify-center gap-2">
            {post.tags.map(tag => (
              <Tag key={tag} label={tag} onClick={() => onTagClick(tag)} />
            ))}
          </div>
        </header>

        {/* Minimalist Markdown rendering: mostly whitespace preservation and simple typography */}
        <div className="prose prose-stone prose-lg mx-auto font-serif text-stone-700 leading-loose whitespace-pre-wrap">
          {post.content}
        </div>

        <div className="mt-16 pt-8 border-t border-stone-200 flex justify-end">
          <Button variant="ghost" onClick={onEdit}>
            <Edit3 size={16} /> Edit Post
          </Button>
        </div>
      </article>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Component: App (Main)
// ---------------------------------------------------------------------------

const STORAGE_KEY = 'zenblog_posts';

// Sample initial data if storage is empty
const SAMPLE_POSTS: BlogPost[] = [
  {
    id: '1',
    title: 'The Art of Minus',
    content: "Minimalism isn't about having less. It's about making room for more of what matters.\n\nIn a world screaming for our attention, silence is a radical act. When we strip away the non-essential, we are left with the raw truth of our existence. It allows us to breathe, to think, and to create without the burden of constant noise.\n\nStart small. Clear a surface. Delete an app. Say no to a commitment that drains you.",
    excerpt: "Minimalism isn't about having less. It's about making room for more of what matters. In a world screaming for our attention...",
    tags: ['minimalism', 'philosophy'],
    createdAt: Date.now() - 100000000,
    updatedAt: Date.now()
  },
  {
    id: '2',
    title: 'Digital Gardens',
    content: "A blog shouldn't be a stream of finished products. It should be a garden.\n\nSome ideas are seeds, barely germinated. Others are saplings, needing care. A few are ancient oaks, standing tall.\n\nTending to a digital garden means revisiting old posts, pruning dead links, and grafting new ideas onto old branches. It is a living, breathing entity.",
    excerpt: "A blog shouldn't be a stream of finished products. It should be a garden. Some ideas are seeds, barely germinated...",
    tags: ['writing', 'digital'],
    createdAt: Date.now() - 50000000,
    updatedAt: Date.now()
  }
];

export default function App() {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [viewState, setViewState] = useState<ViewState>({ type: 'LIST' });

  // Load posts
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        setPosts(JSON.parse(saved));
      } catch (e) {
        console.error("Failed to load posts", e);
        setPosts(SAMPLE_POSTS);
      }
    } else {
      setPosts(SAMPLE_POSTS);
    }
  }, []);

  // Save posts
  useEffect(() => {
    if (posts.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(posts));
    }
  }, [posts]);

  // Navigation Handlers
  const goToList = useCallback((tag?: string) => {
    setViewState({ type: 'LIST', tagFilter: tag });
    window.scrollTo(0, 0);
  }, []);

  const goToPost = useCallback((id: string) => {
    setViewState({ type: 'READ', postId: id });
    window.scrollTo(0, 0);
  }, []);

  const goToEdit = useCallback((id?: string) => {
    setViewState({ type: 'EDIT', postId: id });
    window.scrollTo(0, 0);
  }, []);

  // Action Handlers
  const handleSavePost = (post: BlogPost) => {
    setPosts(prev => {
      const exists = prev.find(p => p.id === post.id);
      if (exists) {
        return prev.map(p => p.id === post.id ? post : p);
      }
      return [post, ...prev];
    });
    setViewState({ type: 'READ', postId: post.id });
  };

  const currentPost = viewState.type === 'READ' || viewState.type === 'EDIT' 
    ? posts.find(p => p.id === viewState.postId) 
    : undefined;

  return (
    <div className="min-h-screen bg-stone-50 text-stone-800 font-sans pb-20">
      {/* Navigation Bar */}
      <nav className="sticky top-0 z-50 bg-stone-50/90 backdrop-blur-sm border-b border-stone-100 mb-12">
        <div className="max-w-3xl mx-auto px-6 h-16 flex items-center justify-between">
          <div 
            className="text-xl font-serif font-bold tracking-tight cursor-pointer select-none"
            onClick={() => goToList()}
          >
            ZenBlog<span className="text-stone-400">.</span>
          </div>
          
          <div className="flex gap-4">
             {viewState.type === 'LIST' && (
              <Button onClick={() => goToEdit()}>
                 <Plus size={18} /> Write
              </Button>
             )}
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="px-6">
        {viewState.type === 'LIST' && (
          <PostList 
            posts={posts} 
            onSelect={goToPost} 
            selectedTag={viewState.tagFilter}
            onTagClick={goToList}
            onClearTag={() => goToList(undefined)}
          />
        )}

        {viewState.type === 'READ' && currentPost && (
          <PostDetail 
            post={currentPost} 
            onBack={() => goToList()} 
            onEdit={() => goToEdit(currentPost.id)}
            onTagClick={goToList}
          />
        )}

        {viewState.type === 'EDIT' && (
          <Editor 
            initialPost={currentPost} 
            onSave={handleSavePost}
            onCancel={() => currentPost ? goToPost(currentPost.id) : goToList()}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="mt-20 py-8 text-center text-stone-400 text-sm">
        <p>&copy; {new Date().getFullYear()} ZenBlog. Minimalist thought engine.</p>
      </footer>
    </div>
  );
}