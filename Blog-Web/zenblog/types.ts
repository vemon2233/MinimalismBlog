export interface BlogPost {
  id: string;
  title: string;
  content: string;
  excerpt: string;
  tags: string[];
  createdAt: number;
  updatedAt: number;
}

export type ViewState = 
  | { type: 'LIST'; tagFilter?: string }
  | { type: 'READ'; postId: string }
  | { type: 'EDIT'; postId?: string };

export interface AIResponse {
  content: string;
  suggestedTags?: string[];
}
