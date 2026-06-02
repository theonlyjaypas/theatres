# Deploy to Render.com (Fastest - 5 minutes)

Deploy your app publicly in **5 minutes** for free with minimal setup.

## ⚡ Quick Deploy

### Step 1: Push to GitHub

First, make sure your code is on GitHub:

```bash
git add .
git commit -m "Add production deployment setup"
git push origin main
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Click **Sign up with GitHub**
3. Authorize Render to access your repos

### Step 3: Create Web Service

1. Click **+ New**
2. Select **Web Service**
3. Connect your `theatres` repository
4. Select the repo and click **Connect**

### Step 4: Configure

Fill in these settings:

| Field | Value |
|-------|-------|
| **Name** | `theatres-dashboard` |
| **Environment** | `Docker` |
| **Region** | `Oregon` (closest to you) |
| **Branch** | `main` |
| **Build Command** | (leave empty) |
| **Start Command** | (leave empty) |

### Step 5: Add Environment Variables

Click **Advanced** → **Add Environment Variable**

Add these:
```
ENVIRONMENT=production
LOG_LEVEL=INFO
PORT=10000
```

### Step 6: Deploy

Click **Create Web Service**

⏳ **Wait 2-3 minutes** while it builds...

### Step 7: Get Your URL

Once deployed, you'll see:
```
https://theatres-dashboard.onrender.com
```

**Share this URL on social media!** 🎉

---

## ✅ Verify It Works

```bash
# Check health
curl https://theatres-dashboard.onrender.com/_stcore/health

# View logs
# In Render dashboard: Logs tab
```

---

## 💰 Pricing

- **Free tier:** ✅ Works great for sharing
  - Auto-sleeps after 15 mins of inactivity
  - Wakes up when someone accesses it
  - Perfect for social media sharing
  
- **Paid ($7/month):** No auto-sleep, always on

**Start free, upgrade if needed!**

---

## 🚀 What Happens Next

1. **First access:** App wakes up (~30 sec)
2. **Data loads:** CSV loaded into memory
3. **Dashboard ready:** Full functionality
4. **Subsequent loads:** Fast (cached in memory)

---

## 🔄 Update Your App

When you make changes:

```bash
git add .
git commit -m "Updated dashboard"
git push origin main
```

Render automatically redeploys in **~2 minutes**.

---

## 📊 Monitor Your Deployment

In Render dashboard:
- **Logs** tab → See errors/startup messages
- **Metrics** tab → Memory, CPU, requests
- **Deployments** tab → View history

---

## ⚠️ Common Issues

**App goes to sleep?**
- Normal on free tier
- First access takes 30 seconds to wake up
- Add a `keep-alive` service or upgrade to paid

**Port error?**
- Render assigns port dynamically
- We use `PORT=10000` but Render overrides it
- **Solution:** Already handled in Dockerfile ✅

**Data file not found?**
- Render copies all files from your repo
- `theaters.csv` must be in repo root
- Check it's committed: `git ls-files | grep theaters.csv`

**Memory error?**
- Free tier has 512MB
- If data is huge, upgrade to paid ($7/month = 1GB)

---

## 🎯 Next: Share on Social Media

Your public URL is ready! Share like:

```
Check out my new Theatre Dashboard! 
Interactive analysis of 1,100+ large-format cinemas worldwide.
https://theatres-dashboard.onrender.com

Explore projector brands, formats, geographic distribution, and more!

#DataViz #Cinema #Dashboard #Streamlit
```

---

## Stuck? Try This

1. Check Render **Logs** tab for errors
2. Verify `theaters.csv` is in repo: `git ls-files`
3. Check GitHub Actions for build errors
4. Try rebuilding: Render dashboard → Deployment → Manual Redeploy

---

## 🆘 Still Having Issues?

Let me know:
- Screenshot of error
- What you see in Logs tab
- URL of your app

I can debug with you! 🔧
