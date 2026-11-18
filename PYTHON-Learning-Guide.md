# Learning Python from the Beginning

This is a beginner-friendly path for learning Python, supported by links to the official Python documentation. The explanations and exercises an AI tutor creates are teaching aids; consult the linked documentation for authoritative language details.

> **About the official tutorial:** The Python Tutorial says it is for programmers who are new to Python, not for people who are new to programming. This learning path uses its official topics, but the tutor should explain programming ideas from the beginning and define unfamiliar terms.
>
> Python documentation describes the language, not every beginner's learning needs. Ask the tutor for smaller steps and more examples whenever needed.

## How the tutor should teach

- Start with one idea at a time and explain unfamiliar words in plain language.
- Use short, runnable examples, but do not complete an exercise for the learner unless they explicitly ask for the solution.
- After presenting an exercise, wait for the learner's attempt. Give hints, point out the relevant concept, and explain errors without taking over.
- If a question is ambiguous, ask what the learner means before choosing an interpretation.
- When a question depends on a version, operating system, package, or command that is not clear, ask for that detail or state the assumption.
- Prefer the official Python documentation as the source of truth. Say when a detail is not covered by this guide instead of guessing.
- Occasionally test understanding with a short question, prediction task, or mini-quiz. Ask the learner to answer before revealing or explaining the answer.
- Adjust difficulty based on the learner's answers and revisit earlier ideas when needed.

## What you will learn

- Read and run small Python programs.
- Recognize common values and data structures.
- Use conditions, loops, and functions.
- Use common built-in functions and understand how to find more in the standard library.
- Run Python from the command line and use basic project commands.
- Read error messages and handle expected errors.
- Split code into modules and use a virtual environment.
- Practise by changing small programs and explaining what changed.

## 1. Run Python and read a small program

Learn the difference between typing an expression at Python's interactive prompt and saving code in a `.py` file. Start with `print()`, comments, and the idea that Python executes instructions.

Practice: print a greeting, then change the text and run it again.

Official reading: [Using the Python interpreter](https://docs.python.org/3/tutorial/interpreter.html) and [An informal introduction to Python](https://docs.python.org/3/tutorial/introduction.html).

## 2. Values, names, and simple expressions

Explore numbers, text (`str`), variables, assignment, arithmetic, and comparisons. A variable name refers to a value; `=` assigns a value to a name.

Begin with built-in functions such as `print()`, `type()`, `len()`, and `input()`. Learn that a function receives arguments and may return a value. Use `help()` and the official documentation to investigate unfamiliar built-ins rather than trying to memorize every function.

Practice: store a name and a number in variables, then print a sentence using them. Before running it, predict the type of each value.

Official reading: [An informal introduction to Python](https://docs.python.org/3/tutorial/introduction.html).

## 3. Make decisions, repeat work, and write functions

Use `if` to choose between paths, loops to repeat work, and functions to give a reusable piece of code a name. Begin with function parameters and `return`; add more function options later.

Practice: write a function that receives a number and returns a result, then call it with two different values.

Official reading: [More control flow tools](https://docs.python.org/3/tutorial/controlflow.html).

## 4. Keep related values in collections

Learn when lists, tuples, sets, and dictionaries are useful. Practise looking up, adding, and iterating over values. Do not try to memorize every collection method at once.

Practice: make a list of three items and a dictionary that associates a name with one piece of information.

Official reading: [Data structures](https://docs.python.org/3/tutorial/datastructures.html).

## 5. Organize code into modules

A module is a Python file that can be imported by another file. Learn how to import a module and why splitting a larger program into files can help organize it.

Practice: put a small function in one file and import it from another file.

Official reading: [Modules](https://docs.python.org/3/tutorial/modules.html).

## 6. Understand errors and work with files

Learn to distinguish syntax errors from exceptions raised while a program runs. Read the exception type and traceback to locate the problem. Practise handling an expected exception. Later, try reading and writing a small text file.

Practice: deliberately cause a simple error, read its type, then correct the cause.

Official reading: [Errors and exceptions](https://docs.python.org/3/tutorial/errors.html) and [Input and output](https://docs.python.org/3/tutorial/inputoutput.html).

## 7. Build a small project in an isolated environment

Bring together functions, collections, modules, and error handling in a small program. Learn what a virtual environment is and why separate projects can use separate installed packages.

Practice: create a small command-line program, run it, and explain what each part does.

Official reading: [Virtual environments and packages](https://docs.python.org/3/tutorial/venv.html) and the [Python Tutorial](https://docs.python.org/3/tutorial/).

## Commands and tools to learn gradually

The tutor may explain commands when they are relevant to the learner's project. Do not assume that a command works the same way in every terminal; ask which operating system and shell are being used when that matters.

- `python --version` or `py --version`: check a Python installation on Windows.
- `python`: open the interactive interpreter.
- `python filename.py`: run a Python file.
- `python -m venv .venv`: create a virtual environment.
- Windows PowerShell activation: `.\.venv\Scripts\Activate.ps1`.
- `python -m pip install package-name`: install a package into the active environment.
- `python -m pip list`: inspect installed packages.
- `python -m pip freeze`: record installed package versions.
- `python -m unittest`: run tests written with the standard-library `unittest` framework.

Use the [Using Python on Windows](https://docs.python.org/3/using/windows.html), [Installing Python modules](https://docs.python.org/3/installing/index.html), and [venv](https://docs.python.org/3/library/venv.html) documentation for command details. The tutor should explain what a command does before asking the learner to run it.

## Built-in functions and the standard library

Study built-ins in small groups and practise looking up their official documentation:

- Inspection and interaction: `print()`, `input()`, `type()`, `isinstance()`, `help()`, `dir()`.
- Conversion and construction: `int()`, `float()`, `str()`, `bool()`, `list()`, `dict()`, `set()`, `tuple()`.
- Working with sequences and values: `len()`, `range()`, `enumerate()`, `zip()`, `sorted()`, `reversed()`, `min()`, `max()`, `sum()`, `any()`, `all()`.
- Safe or explicit decisions: `abs()`, `round()`, and `open()` when file handling has been introduced.

The full reference is the official [Built-in Functions](https://docs.python.org/3/library/functions.html) page. The tutor should introduce only the functions needed for the current exercise and should distinguish built-ins from functions imported from a module.

## Practice and quiz pattern

For each new topic, the tutor should use this sequence:

1. Explain the concept briefly.
2. Show one small example and label it as an example.
3. Ask the learner to change or extend it.
4. Wait for the learner's code or answer.
5. Give feedback, hints, and the next small challenge.

After a few topics, use a short knowledge check with questions such as “What type of value is this?”, “What will this code print?”, or “Which function would you choose and why?” Do not reveal answers until the learner has attempted the questions, unless they request the answer directly.

## Study routine

For each step:

1. Ask for one concept at a time.
2. Read or run a small example.
3. Try changing the example yourself before asking for the answer.
4. When something fails, share the error message and the relevant code; do not share passwords, API keys, or other secrets.
5. Ask the tutor to explain what happened, then retry with a small variation.

The official [Python Tutorial](https://docs.python.org/3/tutorial/) is the main reference for this path. Its table of contents links to additional chapters, including classes and the standard library, when you are ready for them.

Additional official references:

- [Python documentation](https://docs.python.org/3/)
- [The Python Standard Library](https://docs.python.org/3/library/)
- [Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Python Glossary](https://docs.python.org/3/glossary.html)
- [Python FAQ](https://docs.python.org/3/faq/)
