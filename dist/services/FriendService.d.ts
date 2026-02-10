/**
 * Friend Service
 * Handles friend requests and friendship management
 * Requirements: 5.1-5.6
 */
import { User, FriendRequest } from '../models/types';
/**
 * Friend Service Interface
 */
export interface IFriendService {
    sendFriendRequest(fromUserId: string, toUserId: string): Promise<FriendRequest>;
    acceptFriendRequest(requestId: string, userId: string): Promise<void>;
    declineFriendRequest(requestId: string, userId: string): Promise<void>;
    removeFriend(userId: string, friendId: string): Promise<void>;
    getFriends(userId: string): Promise<User[]>;
    areFriends(userId1: string, userId2: string): Promise<boolean>;
}
//# sourceMappingURL=FriendService.d.ts.map