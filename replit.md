# E-Commerce Conversational AI Assistant

## Overview

This is a full-stack conversational AI application built for e-commerce customer support. The system combines a React frontend with an Express.js backend, using PostgreSQL for data persistence and Groq API for AI-powered chat functionality. The application provides a modern, responsive chat interface where users can interact with an AI assistant for product inquiries, order support, and general customer service questions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **Routing**: Wouter for lightweight client-side routing
- **State Management**: React Context API with TanStack React Query for server state
- **UI Framework**: Radix UI components with shadcn/ui design system
- **Styling**: Tailwind CSS with CSS variables for theming
- **Build Tool**: Vite for development and production builds

### Backend Architecture
- **Runtime**: Node.js with Express.js framework
- **Language**: TypeScript with ES modules
- **Database**: PostgreSQL with Drizzle ORM for type-safe database operations
- **Database Connection**: Neon serverless PostgreSQL with connection pooling
- **AI Integration**: Groq API for conversational AI responses
- **Session Management**: Built-in session handling for conversation persistence

### Data Storage Solutions
- **Primary Database**: PostgreSQL hosted on Neon serverless platform
- **ORM**: Drizzle ORM with schema-first approach
- **Migration Strategy**: Drizzle Kit for database schema management
- **Connection Management**: Connection pooling via @neondatabase/serverless

## Key Components

### Database Schema
- **Users Table**: Stores user information with UUID primary keys
- **Conversations Table**: Links to users, stores conversation metadata
- **Messages Table**: Stores individual chat messages with sender identification
- **Products Table**: E-commerce product catalog with full-text search capabilities
- **Relationships**: Proper foreign key constraints with cascade deletion

### Chat System
- **Real-time Messaging**: Context-aware conversation handling
- **AI Integration**: Groq API with Mixtral-8x7b-32768 model
- **Conversation Management**: Persistent chat history and context retention
- **Message Types**: Support for both user and AI messages with timestamps

### UI Components
- **Chat Interface**: Modern messaging UI with typing indicators
- **Sidebar Navigation**: Collapsible conversation history
- **Responsive Design**: Mobile-first approach with adaptive layouts
- **Component Library**: Comprehensive UI components from shadcn/ui

### API Layer
- **RESTful Endpoints**: Standard HTTP methods for CRUD operations
- **Type Safety**: Shared TypeScript schemas between frontend and backend
- **Error Handling**: Centralized error management with proper HTTP status codes
- **Request Validation**: Zod schema validation for API requests

## Data Flow

1. **User Interaction**: User submits message through chat interface
2. **Frontend Processing**: React context manages local state and optimistic updates
3. **API Request**: TanStack Query handles HTTP requests with caching
4. **Backend Processing**: Express routes validate and process requests
5. **Database Operations**: Drizzle ORM manages data persistence
6. **AI Processing**: Groq API generates contextual responses
7. **Response Delivery**: Structured JSON responses sent back to frontend
8. **UI Updates**: Real-time UI updates with smooth animations

## External Dependencies

### Core Framework Dependencies
- **React Ecosystem**: React, React DOM, React Query for state management
- **Backend**: Express.js, TypeScript, ESBuild for compilation
- **Database**: Drizzle ORM, Neon serverless PostgreSQL client
- **UI Libraries**: Radix UI primitives, Lucide React icons

### AI and External Services
- **Groq API**: Large language model integration for conversational AI
- **Environment Configuration**: Environment variables for API keys and database URLs

### Development Tools
- **Build Tools**: Vite for frontend bundling, ESBuild for backend compilation
- **Type Checking**: TypeScript with strict configuration
- **Code Quality**: Path mapping for clean imports, ES modules throughout

## Deployment Strategy

### Build Process
- **Frontend**: Vite builds optimized React application to `dist/public`
- **Backend**: ESBuild compiles TypeScript server code to `dist` directory
- **Database**: Drizzle Kit manages schema migrations and deployments

### Environment Configuration
- **Development**: Local development with Vite dev server and hot reload
- **Production**: Compiled static assets served by Express server
- **Database**: Environment-based configuration for different deployment stages

### Scalability Considerations
- **Database**: Serverless PostgreSQL with automatic scaling
- **Frontend**: Static asset optimization with code splitting
- **Backend**: Stateless server design for horizontal scaling
- **Caching**: React Query provides intelligent client-side caching

The application follows modern full-stack development practices with type safety throughout, comprehensive error handling, and a mobile-responsive user experience optimized for e-commerce customer support scenarios.