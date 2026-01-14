# 📚 Documentation Index

Welcome to the Farmers Market documentation. This index helps you find what you need.

## Quick Navigation

### 🚀 Getting Started
- **New to the project?** → Start with [../README.md](../README.md)
- **Setting up development?** → See `GUIDES/SETUP.md` (coming soon)
- **Quick feature overview?** → See appropriate feature folder below

### 📁 Documentation Structure

```
docs/
├── INDEX.md (this file)
├── FEATURES/
│   ├── multi-image-posts/          ← Upload up to 15 images per post
│   │   ├── 01-QUICK_START.md
│   │   ├── 02-TECHNICAL_REFERENCE.md
│   │   ├── 03-TESTING_GUIDE.md
│   │   ├── 04-IMPLEMENTATION_DETAILS.md
│   │   └── CHANGELOG.md
│   │
│   └── image-uploads/              ← Single image upload feature
│       ├── OVERVIEW.md
│       └── GUIDE.md
│
├── GUIDES/
│   ├── API_REFERENCE.md            ← All API endpoints
│   ├── DATABASE_SCHEMA.md           ← Database structure
│   ├── ARCHITECTURE.md              ← System design
│   └── DEPLOYMENT.md                ← How to deploy
│
└── DESIGN/
    ├── MOBILE_RESPONSIVE.md         ← Mobile design specs
    └── ACCESSIBILITY.md             ← Accessibility guidelines
```

---

## Features

### 📸 Multi-Image Posts Feature
**Status:** ✅ Complete (v1.0.0) | **Last Updated:** Jan 10, 2026 | **Docs Complete:** 4/4 ✅

Upload up to 15 images per post with gallery view and full-screen modal. Fully tested and production-ready.

**Key Stats:** 1-15 images | 5MB max each | JPEG/PNG/GIF/WebP | 23 tests passing | 2 API endpoints | 0 known bugs

**Quick Links:**
- 🚀 [Quick Start](FEATURES/multi-image-posts/01-QUICK_START.md) - 30-sec overview + user guide
- 📖 [Technical Reference](FEATURES/multi-image-posts/02-TECHNICAL_REFERENCE.md) - Architecture, API, DB schema
- 🧪 [Testing Guide](FEATURES/multi-image-posts/03-TESTING_GUIDE.md) - 23 comprehensive test scenarios
- 📝 [Changelog](FEATURES/multi-image-posts/CHANGELOG.md) - What changed & implementation details

**For:**
- 👨‍🌾 Farmers/Users → [Quick Start](FEATURES/multi-image-posts/01-QUICK_START.md) (2 min read)
- 🧪 QA/Testers → [Testing Guide](FEATURES/multi-image-posts/03-TESTING_GUIDE.md) (detailed scenarios)
- 💻 Developers → [Technical Reference](FEATURES/multi-image-posts/02-TECHNICAL_REFERENCE.md) (API, code)
- 🚀 DevOps → [Changelog](FEATURES/multi-image-posts/CHANGELOG.md) (deployment info)

---

### 🖼️ Image Upload Feature
**Status:** ✅ Complete (v1.0.0) | **Archive:** Superseded by Multi-Image

Single image upload feature (predecessor to multi-image). Documents preserved for historical reference.

**Quick Links:**
- 📖 [Overview](FEATURES/image-uploads/OVERVIEW.md) - Feature summary

---

## Development Guides

### API Reference
- All endpoints documented
- Request/response formats
- Error codes and handling
- Authentication requirements

**Path:** [GUIDES/API_REFERENCE.md](GUIDES/API_REFERENCE.md)

### Database Schema
- Table structures
- Relationships
- Migrations
- Indexes

**Path:** [GUIDES/DATABASE_SCHEMA.md](GUIDES/DATABASE_SCHEMA.md)

### Architecture
- System design
- Components
- Data flow
- Performance considerations

**Path:** [GUIDES/ARCHITECTURE.md](GUIDES/ARCHITECTURE.md)

### Deployment
- Prerequisites
- Deployment steps
- Configuration
- Rollback procedures

**Path:** [GUIDES/DEPLOYMENT.md](GUIDES/DEPLOYMENT.md)

---

## Design Documentation

### Mobile Responsive Design
- Breakpoints
- Layout strategies
- Touch-friendly UI
- Performance optimization

**Path:** [DESIGN/MOBILE_RESPONSIVE.md](DESIGN/MOBILE_RESPONSIVE.md)

### Accessibility
- WCAG compliance
- Color contrast
- Keyboard navigation
- Screen reader support

**Path:** [DESIGN/ACCESSIBILITY.md](DESIGN/ACCESSIBILITY.md)

---

## By Role

### 👨‍🌾 Farmer / User
1. Read [../README.md](../README.md) for overview
2. Check feature [Quick Start](FEATURES/multi-image-posts/01-QUICK_START.md)
3. Refer to [GUIDES/DEPLOYMENT.md](GUIDES/DEPLOYMENT.md) if needed

### 🧪 QA / Tester
1. Read feature [Testing Guide](FEATURES/multi-image-posts/03-TESTING_GUIDE.md)
2. Review [DESIGN/MOBILE_RESPONSIVE.md](DESIGN/MOBILE_RESPONSIVE.md)
3. Check [DESIGN/ACCESSIBILITY.md](DESIGN/ACCESSIBILITY.md)

### 👨‍💻 Backend Developer
1. Review [GUIDES/ARCHITECTURE.md](GUIDES/ARCHITECTURE.md)
2. Study [GUIDES/DATABASE_SCHEMA.md](GUIDES/DATABASE_SCHEMA.md)
3. Check [GUIDES/API_REFERENCE.md](GUIDES/API_REFERENCE.md)
4. Reference [FEATURES/multi-image-posts/02-TECHNICAL_REFERENCE.md](FEATURES/multi-image-posts/02-TECHNICAL_REFERENCE.md)

### 🎨 Frontend Developer
1. Review [GUIDES/ARCHITECTURE.md](GUIDES/ARCHITECTURE.md)
2. Check [DESIGN/MOBILE_RESPONSIVE.md](DESIGN/MOBILE_RESPONSIVE.md)
3. Reference [FEATURES/multi-image-posts/02-TECHNICAL_REFERENCE.md](FEATURES/multi-image-posts/02-TECHNICAL_REFERENCE.md)

### 🚀 DevOps / SRE
1. Read [GUIDES/DEPLOYMENT.md](GUIDES/DEPLOYMENT.md)
2. Check [FEATURES/multi-image-posts/CHANGELOG.md](FEATURES/multi-image-posts/CHANGELOG.md)
3. Reference [GUIDES/DATABASE_SCHEMA.md](GUIDES/DATABASE_SCHEMA.md)

### 👔 Project Manager / Stakeholder
1. Read [../README.md](../README.md)
2. Check feature [Quick Start](FEATURES/multi-image-posts/01-QUICK_START.md)
3. Review status in [FEATURES/multi-image-posts/CHANGELOG.md](FEATURES/multi-image-posts/CHANGELOG.md)

---

## Finding Specific Information

### "How do I...?"

| Question | Document |
|----------|----------|
| Use the multi-image feature? | [Quick Start](FEATURES/multi-image-posts/01-QUICK_START.md) |
| Test the feature? | [Testing Guide](FEATURES/multi-image-posts/03-TESTING_GUIDE.md) |
| Call an API endpoint? | [API Reference](GUIDES/API_REFERENCE.md) |
| Deploy to production? | [Deployment](GUIDES/DEPLOYMENT.md) |
| Understand the database? | [Database Schema](GUIDES/DATABASE_SCHEMA.md) |
| Make it mobile-friendly? | [Mobile Responsive](DESIGN/MOBILE_RESPONSIVE.md) |
| Implement a new feature? | [Architecture](GUIDES/ARCHITECTURE.md) |

---

## Document Status

### Complete & Up-to-Date ✅
- [FEATURES/multi-image-posts/01-QUICK_START.md](FEATURES/multi-image-posts/01-QUICK_START.md)
- [FEATURES/multi-image-posts/02-TECHNICAL_REFERENCE.md](FEATURES/multi-image-posts/02-TECHNICAL_REFERENCE.md)
- [FEATURES/multi-image-posts/03-TESTING_GUIDE.md](FEATURES/multi-image-posts/03-TESTING_GUIDE.md)
- [FEATURES/multi-image-posts/CHANGELOG.md](FEATURES/multi-image-posts/CHANGELOG.md)
- [GUIDES/API_REFERENCE.md](GUIDES/API_REFERENCE.md) - ✅ NEW
- [DESIGN/MOBILE_RESPONSIVE.md](DESIGN/MOBILE_RESPONSIVE.md) - ✅ NEW
- [FEATURES/image-uploads/OVERVIEW.md](FEATURES/image-uploads/OVERVIEW.md) - ✅ NEW
- [FILES_ORGANIZED.md](FILES_ORGANIZED.md) - ✅ Organization summary
- [DEBUGGING_ARCHIVE.md](DEBUGGING_ARCHIVE.md) - ✅ Debug reference

### Coming Soon 📋
- [GUIDES/DATABASE_SCHEMA.md](GUIDES/DATABASE_SCHEMA.md)
- [GUIDES/ARCHITECTURE.md](GUIDES/ARCHITECTURE.md)
- [GUIDES/DEPLOYMENT.md](GUIDES/DEPLOYMENT.md)
- [DESIGN/ACCESSIBILITY.md](DESIGN/ACCESSIBILITY.md)

---

## Archive & Organization

### What Was Organized
All scattered `.md` files from the root directory have been organized into logical categories:

- **Multi-Image Posts** (10+ files) → [FEATURES/multi-image-posts/](FEATURES/multi-image-posts/)
- **Image Uploads** (9+ files) → [FEATURES/image-uploads/](FEATURES/image-uploads/)
- **Mobile Design** (7+ files) → [DESIGN/MOBILE_RESPONSIVE.md](DESIGN/MOBILE_RESPONSIVE.md)
- **Debugging** (3+ files) → [DEBUGGING_ARCHIVE.md](DEBUGGING_ARCHIVE.md)
- **API Reference** (NEW) → [GUIDES/API_REFERENCE.md](GUIDES/API_REFERENCE.md)

### Organization Details
See [FILES_ORGANIZED.md](FILES_ORGANIZED.md) for complete mapping of old files to new locations.

---

## File Organization

### Root Level (Keep Minimal)
Only keep essential files:
- `README.md` - Project overview
- `.gitignore` - Git configuration
- `package.json` - Dependencies
- `manage.py` - Django management

### Documentation
All docs moved to `/docs` folder for better organization.

### Code
- `farmers-market/` - Django backend
- `web/` - React frontend

---

## Quick Links

| Shortcut | Links |
|----------|-------|
| 🏠 Home | [../README.md](../README.md) |
| 🚀 Feature Start | [Multi-Image Quick Start](FEATURES/multi-image-posts/01-QUICK_START.md) |
| 🧪 Testing | [Testing Guide](FEATURES/multi-image-posts/03-TESTING_GUIDE.md) |
| 🔧 Technical | [Technical Reference](FEATURES/multi-image-posts/02-TECHNICAL_REFERENCE.md) |
| 📊 Changes | [Changelog](FEATURES/multi-image-posts/CHANGELOG.md) |

---

## Navigation

- **← Back to root:** [../README.md](../README.md)
- **→ Next:** Pick a document from the structure above
- **↑ Up:** Parent directory

---

## Support

**Can't find what you need?**

1. Check the structure above
2. Search for keywords in document names
3. Use Ctrl+F to search within documents
4. Ask in project discussions

---

**Last Updated:** January 10, 2026

**Status:** 📚 Documentation organized and ready to use
