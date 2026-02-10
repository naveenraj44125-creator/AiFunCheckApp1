"use strict";
/**
 * AI Stories Sharing - Main Application Entry Point
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.app = void 0;
const express_1 = __importDefault(require("express"));
const app = (0, express_1.default)();
exports.app = app;
const PORT = process.env.PORT || 3000;
// Middleware
app.use(express_1.default.json());
// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});
// API routes will be added in Task 12
// Start server
if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`AI Stories Sharing server running on port ${PORT}`);
    });
}
//# sourceMappingURL=index.js.map