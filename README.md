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
Open the Integrated Terminal in VS Code:
You can open the terminal in VS Code by pressing Ctrl + ` (backtick) or by going to the menu and selecting Terminal > New Terminal.
Navigate to Your Project Directory:
If you're not already in your project directory, use the cd command to navigate there. For example:
```sh
     cd D:\Repos\VisionAPI
```
Remove the .git Directory:
Use the Remove-Item cmdlet to delete the .git directory:

```sh
     Remove-Item -Recurse -Force .git
```
