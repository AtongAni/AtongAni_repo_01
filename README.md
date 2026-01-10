# 🌾 Farmers Market App

A Django + React application connecting local farmers with customers. Browse fresh produce, upload multiple product photos, and manage your posts.

## 📚 Documentation

**👉 Start here:** [/docs/INDEX.md](/docs/INDEX.md) - Master documentation hub

All documentation has been organized in the `/docs` folder for better navigation:

### 📁 Structure
```
/docs/
├── INDEX.md                    ← START HERE: Master navigation
├── FEATURES/
│   ├── multi-image-posts/     ← Upload 1-15 images per post ✅
│   └── image-uploads/         ← Single image uploads
├── GUIDES/
│   ├── API_REFERENCE.md       ← All endpoints documented
│   ├── DATABASE_SCHEMA.md     ← Coming soon
│   ├── ARCHITECTURE.md        ← Coming soon
│   └── DEPLOYMENT.md          ← Coming soon
└── DESIGN/
    ├── MOBILE_RESPONSIVE.md   ← Coming soon
    └── ACCESSIBILITY.md       ← Coming soon
```

### 🎯 Quick Links by Role

**👨‍🌾 Farmers/Users:**
- [How to upload product photos](/docs/FEATURES/multi-image-posts/01-QUICK_START.md)

**🧪 QA/Testers:**
- [Testing procedures](/docs/FEATURES/multi-image-posts/03-TESTING_GUIDE.md)

**💻 Developers:**
- [API Reference](/docs/GUIDES/API_REFERENCE.md)
- [Technical Details](/docs/FEATURES/multi-image-posts/02-TECHNICAL_REFERENCE.md)

**🚀 DevOps:**
- [Changelog & Deployment](/docs/FEATURES/multi-image-posts/CHANGELOG.md)

## ✨ Current Features

- ✅ **Multi-Image Posts** - Upload 1-15 images per post with gallery view
- ✅ **User Accounts** - Create account, login, manage posts
- ✅ **Product Feed** - Browse all posted products
- ✅ **Shopping Cart** - Add items to cart
- ✅ **Comments** - Leave feedback on products
- ✅ **Mobile Responsive** - Works on phones, tablets, desktops

## 🏗️ Project Structure

```
app/
├── farmers-market/          ← Django backend
│   ├── posts/              ← Post & image models/APIs
│   ├── accounts/           ← User authentication
│   ├── cart/               ← Shopping cart
│   ├── comments/           ← Product comments
│   └── config/             ← Django settings
│
└── web/                    ← React frontend
    ├── src/
    │   ├── api/            ← API client functions
    │   ├── components/     ← React components
    │   └── pages/          ← Page components
    └── public/             ← Static assets
```

## 🚀 Getting Started

### Backend Setup
```bash
cd farmers-market
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd web
npm install
npm run dev
```

**Full setup instructions:** See [farmers-market/SETUP_INSTRUCTIONS.md](/farmers-market/SETUP_INSTRUCTIONS.md)

## 🔧 Tech Stack

**Backend:**
- Django 6.0
- Django REST Framework
- SQLite (development)
- Pillow (image processing)

**Frontend:**
- React 19
- Vite
- Axios
- CSS Grid/Flexbox

## 📊 Status

| Feature | Status | Docs |
|---------|--------|------|
| Multi-Image Posts | ✅ Complete | [Full docs](/docs/FEATURES/multi-image-posts/) |
| User Accounts | ✅ Complete | [In progress] |
| Shopping Cart | ✅ Complete | [In progress] |
| Comments | ✅ Complete | [In progress] |
| API Reference | ✅ Complete | [API_REFERENCE.md](/docs/GUIDES/API_REFERENCE.md) |

## 🆘 Need Help?

1. **Can't find documentation?** → [/docs/INDEX.md](/docs/INDEX.md)
2. **API questions?** → [/docs/GUIDES/API_REFERENCE.md](/docs/GUIDES/API_REFERENCE.md)
3. **How to test?** → [/docs/FEATURES/multi-image-posts/03-TESTING_GUIDE.md](/docs/FEATURES/multi-image-posts/03-TESTING_GUIDE.md)
4. **Setup issues?** → [farmers-market/SETUP_INSTRUCTIONS.md](/farmers-market/SETUP_INSTRUCTIONS.md)

## 📝 License

This project is a startup/educational project.

## 👥 Contributors

Development team - January 2026

---

**Last Updated:** January 10, 2026 | **Documentation:** [Complete](/docs/INDEX.md)
