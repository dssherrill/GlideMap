# Deployment Guide

This document explains how to keep the GitHub Pages deployment synchronized with the GlideMap repository.

## Automated Deployment (Recommended)

The repository uses GitHub Actions to automatically deploy changes to the GitHub Pages site at https://dssherrill.github.io/GlideRange.html.

### How It Works

1. When changes are pushed to the `main` branch, a GitHub Actions workflow is triggered
2. The workflow copies the necessary files to the `dssherrill/dssherrill.github.io` repository
3. The changes are automatically committed and pushed to the GitHub Pages repository
4. GitHub Pages automatically publishes the updated site

### Setup Requirements

To enable automated deployment, you need to:

1. **Create a Personal Access Token (PAT):**
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give it a descriptive name like "GlideMap Pages Deploy"
   - Select the following scopes:
     - `repo` (Full control of private repositories)
     - `workflow` (Update GitHub Action workflows)
   - Set an appropriate expiration date
   - Click "Generate token" and copy the token

2. **Add the token as a repository secret:**
   - Go to the GlideMap repository on GitHub
   - Navigate to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `PAGES_DEPLOY_TOKEN`
   - Value: Paste the Personal Access Token you created
   - Click "Add secret"

3. **Enable GitHub Actions:**
   - Go to the Actions tab in the GlideMap repository
   - If prompted, enable GitHub Actions for the repository

### Files Deployed

The workflow automatically deploys the following files:
- `GlideRange.html` - Main application file
- `glideRange.js` - JavaScript logic
- `jquery.csv.js` - CSV parsing library
- `Sterling, Massachusetts 2021 SeeYou.cup` - Sample data file
- `LICENSE` - License file

### Manual Trigger

You can also manually trigger the deployment:
1. Go to the Actions tab in the GlideMap repository
2. Select the "Deploy to GitHub Pages" workflow
3. Click "Run workflow"
4. Select the branch (usually `main`)
5. Click "Run workflow"

## Manual Deployment (Alternative)

If you need to manually deploy changes without using GitHub Actions:

### Option 1: Using Git Commands

```bash
# Clone both repositories
git clone https://github.com/dssherrill/GlideMap.git
git clone https://github.com/dssherrill/dssherrill.github.io.git

# Copy files from GlideMap to the Pages repository
cp GlideMap/GlideRange.html dssherrill.github.io/
cp GlideMap/glideRange.js dssherrill.github.io/
cp GlideMap/jquery.csv.js dssherrill.github.io/
cp "GlideMap/Sterling, Massachusetts 2021 SeeYou.cup" dssherrill.github.io/
cp GlideMap/LICENSE dssherrill.github.io/

# Commit and push the changes
cd dssherrill.github.io
git add .
git commit -m "Update GlideRange application from GlideMap repository"
git push origin main
```

### Option 2: Using a Deployment Script

Create a script named `deploy.sh` in your local GlideMap repository:

```bash
#!/bin/bash
set -e

# Configuration
GLIDE_MAP_DIR="."
PAGES_REPO_DIR="../dssherrill.github.io"

# Check if the pages repository exists
if [ ! -d "$PAGES_REPO_DIR" ]; then
    echo "Error: GitHub Pages repository not found at $PAGES_REPO_DIR"
    echo "Please clone it first: git clone https://github.com/dssherrill/dssherrill.github.io.git"
    exit 1
fi

# Copy files
echo "Copying files to GitHub Pages repository..."
cp "$GLIDE_MAP_DIR/GlideRange.html" "$PAGES_REPO_DIR/"
cp "$GLIDE_MAP_DIR/glideRange.js" "$PAGES_REPO_DIR/"
cp "$GLIDE_MAP_DIR/jquery.csv.js" "$PAGES_REPO_DIR/"
cp "$GLIDE_MAP_DIR/Sterling, Massachusetts 2021 SeeYou.cup" "$PAGES_REPO_DIR/"
cp "$GLIDE_MAP_DIR/LICENSE" "$PAGES_REPO_DIR/"

# Commit and push
cd "$PAGES_REPO_DIR"
echo "Committing changes..."
git add .
git commit -m "Update GlideRange application (deployed from GlideMap)" || echo "No changes to commit"
echo "Pushing to GitHub..."
git push origin main
echo "Deployment complete!"
```

Make the script executable: `chmod +x deploy.sh`

Then run it: `./deploy.sh`

## Verification

After deployment (automatic or manual), verify the changes:

1. Wait a few minutes for GitHub Pages to rebuild
2. Visit https://dssherrill.github.io/GlideRange.html
3. Hard refresh your browser (Ctrl+F5 or Cmd+Shift+R) to bypass cache
4. Verify that your changes are visible

## Troubleshooting

### Workflow Fails with Authentication Error
- Verify that the `PAGES_DEPLOY_TOKEN` secret is correctly set
- Check that the Personal Access Token hasn't expired
- Ensure the token has the correct permissions (`repo` and `workflow`)

### Changes Don't Appear on the Site
- Check the GitHub Pages repository to confirm files were updated
- Clear your browser cache or use hard refresh
- Check the GitHub Pages settings in the dssherrill.github.io repository
- Wait a few minutes - GitHub Pages can take time to rebuild

### Workflow Doesn't Trigger
- Ensure you're pushing to the `main` branch
- Check that GitHub Actions is enabled for the repository
- Look at the Actions tab for any error messages

### File Not Found Errors
- Verify that all required files exist in the GlideMap repository
- Check for typos in file names (especially the CUP file with spaces)

## Best Practices

1. **Test locally first**: Always test changes locally before pushing to main
2. **Review workflow runs**: Check the Actions tab after pushing to ensure deployment succeeded
3. **Keep token secure**: Never commit the Personal Access Token to the repository
4. **Update token expiration**: Set a reminder to renew the PAT before it expires
5. **Use descriptive commit messages**: This helps track which changes were deployed when

## Security Considerations

- The Personal Access Token provides access to your repositories - keep it secure
- Use the minimum necessary permissions for the token
- Consider using environment-specific tokens for different purposes
- Rotate tokens regularly
- Review the workflow logs to ensure no sensitive data is being exposed

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Managing Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
