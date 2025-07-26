# E-Commerce Conversational AI Assistant

A full-stack conversational AI application built for e-commerce customer support. Features a React frontend with Express.js backend, PostgreSQL database integration, and authentic clothing product data from 7,400+ real fashion items.

## 🚀 Features

- **Real-time Chat Interface**: Modern messaging UI with conversation history
- **AI-Powered Responses**: Groq API integration with product-aware recommendations
- **Authentic Product Data**: 7,400+ clothing items from major brands (Tommy Hilfiger, Canada Goose, Roxy, Bali)
- **Smart Product Search**: Enhanced search with relevance scoring and brand prioritization
- **Responsive Design**: Mobile-first approach with dark/light theme support
- **Session Management**: Persistent conversation history and context retention

## 📋 Prerequisites

Before running the application, ensure you have:

- **Node.js** (version 18+ recommended)
- **PostgreSQL** database
- **Groq API Key** for AI functionality

## 🛠️ Installation & Setup

### 1. Clone and Install Dependencies

```bash
# Install all dependencies
npm install
```

### 2. Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_URL=your_postgresql_connection_string

# AI Service Configuration
GROQ_API_KEY=your_groq_api_key_here

# Development Environment
NODE_ENV=development
```

### 3. Database Setup

The application uses PostgreSQL with Drizzle ORM. Run the following commands to set up the database:

```bash
# Push database schema
npm run db:push
```

### 4. Load E-Commerce Dataset

Load the authentic clothing dataset into your database:

```bash
# Navigate to server directory and run the data loader
cd server
python load_ecommerce_data.py
cd ..
```

This will populate your database with 7,400+ real clothing products from brands like:
- Tommy Hilfiger (Sweaters, Suits, Tops)
- Canada Goose (Outerwear, Jackets)
- Roxy (Fashion Hoodies, Swimwear)
- Bali (Intimates)
- ASICS (Athletic wear)
- And many more...

## 🚦 Running the Application

### Development Mode

Start the application in development mode:

```bash
npm run dev
```

This command will:
- Start the Express.js backend server on port 5000
- Launch the Vite development server for the React frontend
- Enable hot reload for both frontend and backend
- Serve the application at `http://localhost:5000`

### Production Build

For production deployment:

```bash
# Build the application
npm run build

# Start the production server
npm start
```

## 🎯 How to Use

1. **Open your browser** and navigate to `http://localhost:5000`
2. **Start chatting** with the AI assistant
3. **Ask about products**: Try queries like:
   - "Show me some Tommy Hilfiger sweaters"
   - "I need a winter jacket from Canada Goose"
   - "What dresses do you have?"
   - "Find me athletic wear"
4. **Get personalized recommendations** based on real inventory data

## 🏗️ Project Structure

```
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── contexts/       # React contexts
│   │   ├── hooks/          # Custom hooks
│   │   ├── pages/          # Application pages
│   │   └── lib/            # Utilities and API client
├── server/                 # Express.js backend
│   ├── index.ts           # Server entry point
│   ├── routes.ts          # API routes
│   ├── storage.ts         # Database operations
│   ├── db.ts              # Database connection
│   └── load_ecommerce_data.py  # Data loader script
├── shared/                # Shared TypeScript schemas
└── data/                  # E-commerce dataset files
```

## 🔧 API Endpoints

- `POST /api/users` - Create/authenticate user sessions
- `GET /api/conversations/:userId` - Retrieve conversation history
- `POST /api/chat` - Send messages and get AI responses
- `GET /api/products` - Browse product catalog
- `GET /api/products/search` - Search products

## 🛡️ Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `GROQ_API_KEY` | API key for Groq AI service | Yes |
| `NODE_ENV` | Environment mode (development/production) | No |

## 🎨 Key Technologies

### Frontend
- **React 18** with TypeScript
- **Wouter** for lightweight routing
- **TanStack React Query** for server state management
- **Radix UI** + **shadcn/ui** for components
- **Tailwind CSS** for styling
- **Vite** for build tooling

### Backend
- **Express.js** with TypeScript
- **Drizzle ORM** for database operations
- **PostgreSQL** for data persistence
- **Groq API** for AI chat functionality

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify your `DATABASE_URL` is correct
   - Ensure PostgreSQL is running
   - Run `npm run db:push` to sync schema

2. **AI Responses Not Working**
   - Check your `GROQ_API_KEY` is valid
   - Verify the API key has proper permissions
   - Check server logs for API errors

3. **No Products Showing**
   - Run the data loader: `python server/load_ecommerce_data.py`
   - Verify products were inserted: Check database tables
   - Ensure search functionality is working

4. **Port Already in Use**
   - Kill existing processes on port 5000
   - Or modify the port in `server/index.ts`

### Getting Help

If you encounter issues:
1. Check the browser console for frontend errors
2. Review server logs in the terminal
3. Verify all environment variables are set correctly
4. Ensure all dependencies are installed

## 📝 Development Notes

- The application uses in-memory session storage for development
- Product search includes relevance scoring for better results
- AI responses are enhanced with real product context
- All UI components follow shadcn/ui design patterns
- Database schema is managed through Drizzle migrations

## 🚀 Deployment

The application is ready for deployment on platforms like:
- Replit (recommended)
- Vercel
- Railway
- Heroku

Make sure to:
1. Set all environment variables in your deployment platform
2. Run database migrations
3. Load the product dataset
4. Configure proper CORS settings for production

---

**Happy chatting with your AI fashion assistant!** 🛍️✨