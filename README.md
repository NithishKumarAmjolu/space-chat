# Space Chat Application

A modern, feature-rich chat application built with Django and WebSocket technology. This application provides both one-on-one and group chat capabilities with a sleek, responsive UI.

## Pages and Features

### 1. Home Page (home.html)
![Home Page](https://raw.githubusercontent.com/NithishKumarAmjolu/space-chat/refs/heads/main/images/1.png)

**Features:**
- User welcome header with nickname display
- Friend list with online/offline status indicators
- Friend request management system
- Search functionality for finding users
- Navigation to groups and logout options

**Implementation Details:**
- Built using HTML5 and CSS3 with a modern dark theme
- Real-time online status updates using WebSocket
- Responsive design that adapts to different screen sizes
- Glassmorphism UI effects with custom animations
- Custom button designs with hover and active states

### 2. Chat Room (chat_room.html)
![Home Page](https://raw.githubusercontent.com/NithishKumarAmjolu/space-chat/refs/heads/main/images/Screenshot%20(3).png)

**Features:**
- Real-time one-on-one chat interface
- Message read status indicators (✓ for sent, ✓✓ for read)
- Online/offline status display
- Typing indicators
- Message timestamps
- Auto-scroll to latest messages

**Implementation Details:**
- WebSocket implementation for real-time messaging
- Custom message bubbles with gradient effects
- Automatic reconnection handling
- Message persistence
- Responsive layout for mobile devices
- Custom scrollbar styling

### 3. Group Chat Room (group_chat_room.html)
### 1. Home Page (home.html)
![Home Page](https://raw.githubusercontent.com/NithishKumarAmjolu/space-chat/refs/heads/main/images/Screenshot%20(3).png)


**Features:**
- Real-time group messaging
- Member list sidebar with online status
- Host identification with special badge
- Group ID display for hosts
- Typing indicators for multiple users
- Message sender identification

**Implementation Details:**
- Advanced WebSocket handling for group communications
- Separate chat and members containers
- Dynamic typing indicator for multiple users
- Gradient border animations
- Responsive design with mobile-first approach
- Member list management

### 4. Login Page (LoginPage.html)

**Features:**
- User authentication interface
- Username and password input fields
- Error message display
- Sign up link for new users
- Animated card design

**Implementation Details:**
- Modern gradient background with blur effect
- Card hover animations and glow effects
- Custom form input styling with icons
- Responsive error handling
- Mobile-optimized layout
- Custom button animations with gradient effects

### 5. Sign Up Page (signup.html)

**Features:**
- User registration interface
- Form validation with error messages
- Password requirements help text
- Login link for existing users
- Animated card design with hover effects

**Implementation Details:**
- Gradient background with blur overlay
- Custom form styling with labeled fields
- Real-time validation feedback
- Responsive error handling
- Help text for password requirements
- Smooth animations and transitions
- Mobile-optimized layout

### 6. Search Users (search_users.html)

**Features:**
- User search functionality by username or nickname
- Real-time search results display
- Friend request sending capability
- User information display with nicknames and usernames
- No results handling with appropriate messages
- Back to home navigation

**Implementation Details:**
- Clean search interface with instant feedback
- Glassmorphism design for search bar and results
- Hover animations on user cards
- Custom styling for user information display
- Responsive grid layout for search results
- Error and success message handling
- Mobile-optimized search experience

### 7. My Groups (my_groups.html)

**Features:**
- Overview of hosted and joined groups
- Group creation and joining options
- Group information display (name, ID, member count)
- Quick access to group chats
- Host information for joined groups
- Empty state handling for no groups

**Implementation Details:**
- Separate sections for hosted and joined groups
- Glassmorphism design for group cards
- Interactive hover effects on group items
- Quick action buttons for group management
- Responsive grid layout for group lists
- Custom styling for group metadata
- Mobile-optimized group management interface

### 8. Join Group (join_group.html)

**Features:**
- Group joining interface
- Group ID input field
- Help text for user guidance
- Error/success message handling
- Navigation back to home
- Form validation

**Implementation Details:**
- Clean, focused form design
- Glassmorphism styling for form container
- Helpful input guidance
- Custom form field styling with focus effects
- Responsive error handling
- Mobile-optimized layout
- Smooth animations and transitions

### 9. Create Group (create_group.html)

**Features:**

## WebSocket Implementation

### Chat Consumer (consumers.py)

**Core Functionality:**
- Real-time bidirectional communication
- Message handling and persistence
- Typing indicator management
- Read status tracking
- Online/offline status updates

**Features:**
- Secure chat access verification
- Automatic group management for chat rooms
- Database synchronization for messages
- Real-time typing indicators
- Message read status updates
- Online status tracking
- Error handling and logging

**Implementation Details:**
- Asynchronous WebSocket consumer using Django Channels
- Room-based group chat system
- Database operations using `database_sync_to_async`
- JSON-based message protocol
- Automatic connection/disconnection handling
- User authentication verification
- Channel layer group management

**Message Types:**
- Chat messages with sender info
- Typing status notifications
- Read status updates
- Online/offline status updates

**Security Features:**
- User authentication check
- Chat access verification
- Secure group management
- Error handling and logging
- Database operation safety

### Group Chat Consumer (group_chat_consumers.py)

**Core Functionality:**
- Real-time group messaging system
- Member status management
- Typing indicators for multiple users
- Message persistence in groups
- Member verification

**Features:**
- Group-based chat rooms
- Member access verification
- Nickname display in messages
- Real-time typing indicators for groups
- Comprehensive logging system
- Member online status tracking

**Implementation Details:**
- Asynchronous WebSocket consumer for group chats
- Dynamic room group management
- Database operations with error handling
- Member verification system
- Nickname resolution for messages
- Detailed logging for debugging
- Status management for group members

**Message Types:**
- Group chat messages with sender details
- Group typing indicators
- Member status updates
- System notifications

**Security Features:**
- Group membership verification
- User authentication checks
- Secure message handling
- Error logging and monitoring
- Database operation safety
- Member access control

### 9. Create Group (create_group.html)

**Features:**
- Simple group creation interface
- Group name input
- Navigation back to home
- Error/success message display

**Implementation Details:**
- Clean, minimalist form design
- Form validation
- Glassmorphism effect on containers
- Responsive button animations
- Error handling with visual feedback
- Custom input field styling

## Common Design Elements

### Styling:
- Dark theme with `#100720` base color
- Glassmorphism effects using `backdrop-filter`
- Gradient animations for borders
- Custom button designs with hover effects
- Responsive layouts for all screen sizes

### Interactive Elements:
- Animated buttons with glow effects
- Custom form inputs with focus states
- Smooth transitions and animations
- Loading states and error handling

### Technical Features:
- WebSocket connections for real-time updates
- Automatic reconnection handling
- Cross-browser compatibility
- Mobile-responsive design
- Error handling and user feedback

## Technologies Used
- HTML5
- CSS3
- JavaScript (ES6+)
- WebSocket Protocol
- Django (Backend)
- SQLite (Database)

## Dependencies

### Core Framework
- Django >= 5.0.0 - Main web framework
- Channels >= 4.0.0 - WebSocket handling
- Daphne >= 4.0.0 - ASGI server
- Channels Redis >= 4.1.0 - Channel layer backend

### WebSocket Implementation
- WebSockets >= 11.0.0 - WebSocket protocol support
- Autobahn >= 23.0.0 - WebSocket components
- Twisted >= 23.0.0 - Event-driven networking engine
- Txaio >= 23.0.0 - Async/await support

### Security
- Cryptography >= 41.0.0 - Cryptographic recipes
- PyOpenSSL >= 23.0.0 - TLS/SSL support
- Service Identity >= 23.0.0 - Service identity verification

### Additional Features
- Django CORS Headers >= 4.3.0 - Cross-Origin Resource Sharing
- Django Crispy Forms >= 2.0 - Form rendering
- Python Dotenv >= 1.0.0 - Environment variable management

## Responsive Design
All pages are fully responsive and optimized for:
- Desktop (1024px and above)
- Tablet (768px to 1023px)
- Mobile (below 768px)

Custom breakpoints ensure optimal viewing experience across all devices with specific style adjustments for each screen size.
