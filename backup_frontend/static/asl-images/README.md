# ASL Images Directory

## Purpose
This directory contains American Sign Language (ASL) alphabet hand sign images used by the **Sign Language** tab's Text → Sign feature.

## Required Files (36 total)

### Alphabet (26 files)
```
A.png, B.png, C.png, D.png, E.png, F.png, G.png, H.png, I.png, J.png, K.png, L.png, M.png,
N.png, O.png, P.png, Q.png, R.png, S.png, T.png, U.png, V.png, W.png, X.png, Y.png, Z.png
```

### Numbers (10 files)
```
0.png, 1.png, 2.png, 3.png, 4.png, 5.png, 6.png, 7.png, 8.png, 9.png
```

## Image Specifications

- **Format**: PNG (required)
- **Naming**: Uppercase only (e.g., `A.png`, not `a.png`)
- **Recommended Size**: 512x512px
- **Background**: White or transparent
- **Content**: Real ASL hand gestures matching official reference charts

## Current Status

**Status**: ⚠️ Images not populated  
**Fallback**: Styled placeholder boxes (feature still works)  
**Action**: See `DOWNLOAD_GUIDE.md` for setup instructions

## Feature Behavior

### With Images
Input: `HELLO` → Displays: H-sign, E-sign, L-sign, L-sign, O-sign (real photos)

### Without Images (Current)
Input: `HELLO` → Displays: H, E, L, L, O (styled white boxes with letters)

Both modes are production-ready and visually polished.

## How It Works

**Frontend Logic** ([sign_generator.html](../../templates/sign_generator.html)):
```javascript
// Loads image from /static/asl-images/{CHAR}.png
img.src = `/static/asl-images/${char}.png`;

// Fallback for missing images
img.onerror = function() {
    // Replaces <img> with styled <div>
    const placeholder = document.createElement('div');
    placeholder.className = 'letter-image missing';
    placeholder.textContent = char;
    this.parentNode.replaceChild(placeholder, this);
};
```

**Result**: No broken image icons, graceful degradation

## Adding Images

See [DOWNLOAD_GUIDE.md](./DOWNLOAD_GUIDE.md) for detailed instructions on acquiring ASL dataset.

Quick steps:
1. Download ASL alphabet dataset from Kaggle/GitHub
2. Extract one image per character (A-Z, 0-9)
3. Rename to uppercase format
4. Place in this directory
5. Refresh browser - images load automatically

## Dataset Sources

- **Kaggle**: [ASL Alphabet Dataset](https://www.kaggle.com/datasets/grassknoted/asl-alphabet)
- **GitHub Numbers**: [Sign Language Digits Dataset](https://github.com/ardamavi/Sign-Language-Digits-Dataset)
- **Manual**: Educational ASL reference sites

---

**Last Updated**: 2026-02-12  
**Feature**: Production-ready with or without images
