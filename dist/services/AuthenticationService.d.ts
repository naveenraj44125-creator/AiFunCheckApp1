/**
 * Authentication Service
 * Handles user registration, login, logout, and session management
 * Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7
 */
import { User, Session } from '../models/types';
/**
 * Authentication Service Interface
 */
export interface IAuthenticationService {
    register(email: string, username: string, password: string): Promise<User>;
    login(email: string, password: string): Promise<Session>;
    logout(sessionId: string): Promise<void>;
    validateSession(sessionId: string): Promise<User | null>;
}
//# sourceMappingURL=AuthenticationService.d.ts.map