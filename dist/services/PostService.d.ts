/**
 * Post Service
 * Handles post creation, retrieval, update, and deletion
 * Requirements: 2.1-2.11, 3.1-3.6, 6.1-6.6
 */
import { Post, PostContent, PostUpdate, Visibility, ValidationResult } from '../models/types';
/**
 * Post Service Interface
 */
export interface IPostService {
    createPost(userId: string, content: PostContent, visibility?: Visibility): Promise<Post>;
    getPost(postId: string, requesterId: string | null): Promise<Post | null>;
    updatePost(postId: string, userId: string, updates: PostUpdate): Promise<Post>;
    deletePost(postId: string, userId: string): Promise<void>;
    validateContent(content: PostContent): ValidationResult;
}
//# sourceMappingURL=PostService.d.ts.map