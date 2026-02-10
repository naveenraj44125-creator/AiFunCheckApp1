/**
 * Feed Service
 * Handles feed generation and post visibility
 * Requirements: 4.1-4.6
 */
import { Post, Pagination, FeedResult } from '../models/types';
/**
 * Feed Service Interface
 */
export interface IFeedService {
    getFeed(userId: string | null, pagination: Pagination): Promise<FeedResult>;
    canViewPost(post: Post, viewerId: string | null, friendsList: string[]): boolean;
}
//# sourceMappingURL=FeedService.d.ts.map