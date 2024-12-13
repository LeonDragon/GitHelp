# Vision AI App with Bootstrap UI

This project is a Vision AI application with a Bootstrap-based user interface. Follow the steps below to initialize a Git repository, set up a `.gitignore` file, and push your project to GitHub.

## Getting Started

### Initialize a Git Repository

1. Open a terminal in your project directory.
2. Run the following command to initialize a Git repository:
```sh
git init
```

### Create a .gitignore File

1. Create a file named `.gitignore` in your project root.
2. Add the following content to the `.gitignore` file to prevent unnecessary files from being tracked by Git:

```sh
plaintext
pycache/
*.pyc
venv/
.env
*.log
credentials/
secrets/
static/uploads/
```


### Add and Commit Your Files

1. Add your files to the staging area:

```sh
git add .
```

2. Commit your changes:

```sh
git commit -m "Initial commit: Vision AI App with Bootstrap UI"
```

### Create a New Repository on GitHub

1. Go to [GitHub](https://github.com/).
2. Click on the "+" icon in the top right corner and select "New repository".
3. Name your repository (e.g., "vision-ai-app").
4. Choose whether to make it public or private.
5. Do not initialize the repository with a README, .gitignore, or license.

### Link Your Local Repository to GitHub

1. Replace `<your-username>` and `<repository-name>` with your GitHub username and the name you gave your repository.
2. Run the following command to link your local repository to the GitHub repository:

```sh
git remote add origin https://github.com/<your-username>/<repository-name>.git
```


### Push Your Code to GitHub

1. Push your code to GitHub:

```sh
git push -u origin master
```

2. Verify the push by going to your GitHub repository page and refreshing. You should see your code there.

## Additional Tips

- **Sensitive Information**: Make sure you don't push any sensitive information like API keys or credentials. Double-check your `.gitignore` file to ensure such files are not tracked.
- **Virtual Environment**: If you're using a virtual environment, don't push it to GitHub. Instead, include a `requirements.txt` file with your project dependencies.
- **Project Documentation**: You can create a `README.md` file in your project root to provide information about your project, how to set it up, and how to use it.

After following these steps, your Vision AI App with the updated Bootstrap UI should be successfully pushed to GitHub. You can now easily share your project or collaborate with others.

## Exception Handling
1. Open the Integrated Terminal in VS Code:
- You can open the terminal in VS Code by pressing Ctrl + ` (backtick) or by going to the menu and selecting Terminal > New Terminal.
2. Navigate to Your Project Directory:
- If you're not already in your project directory, use the cd command to navigate there. For example:
```sh
     cd D:\Repos\VisionAPI
```
3. Remove the .git Directory:
- Use the Remove-Item cmdlet to delete the .git directory:

```sh
     Remove-Item -Recurse -Force .git
```

# How to Work with the `beta2` Branch

Follow these steps to create, commit changes, and push to the `beta2` branch in your repository.

## 1. Create the `beta2` Branch Locally
If the `beta2` branch does not exist locally, create it:

```bash
git checkout -b beta2
```

## 2. Stage and Commit Your Changes
If you have uncommitted changes, stage and commit them:

```bash
git add .
git commit -m "Added files for beta2 branch"
```

## 3. Push the Branch to Remote
Push the newly created branch to the remote repository and set it to track:

```bash
git push -u origin beta2
```

## 4. Verify the Push
Go to your GitHub repository and check if the `beta2` branch now exists and contains your changes.

---

## If the Branch Already Exists Remotely
If the `beta2` branch already exists on GitHub but not locally:

```bash
git fetch origin
git checkout beta2
```

Then push your changes:

```bash
git add .
git commit -m "Updated beta2 branch with new files"
git push
```


