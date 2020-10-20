---
title: Developing a Single Page App with FastAPI and React
layout: blog
share: true
toc: true
permalink: fastapi-mongo
type: blog
author: Abdulazeez Abdulazeez Adeshina
lastname: adeshina
description: This tutorial looks at how to develop an asynchronous API with FastAPI and MongoDB.
keywords: "fastapi, python fastapi, fastapi mongo, fastapi mongodb, fastapi rest api"
image: fastapi-mongo/fastapi_mongo.png
topics: "fastapi, api, heroku"
blurb: Develop an asynchronous API with FastAPI and MongoDB.
related_posts: fastapi-crud, fastapi-machine-learning, fastapi-streamlit
featured_course: tdd-fastapi
date: 2020-09-21
modified_date: 2020-09-21
---

In this tutorial, you'll be building a CRUD todo application with [FastAPI](https://fastapi.tiangolo.com/) and [React](https://reactjs.org/). We'll start by scaffolding a new React application with the [Create React App](https://create-react-app.dev/) CLI before building the backend RESTful API with FastAPI.

*Final app*:

![todo application](https://res.cloudinary.com/adeshina/image/upload/v1603073714/j7toccssbwjtvma3sk1m.gif)

*Dependencies:*

- React v16.13.1
- Create React App v3.4.1
- Node v12.1.0
- npm v6.14.0
- npx v6.14.8
- FastAPI v0.61.1
- Python v3.9

> Before beginning this tutorial, you should be familiar with how React works. For a quick refresher on React review the [Main Concepts](https://reactjs.org/docs/hello-world.html) guide or the [Intro to React](https://reactjs.org/tutorial/tutorial.html) tutorial.

## Objectives

By the end of this tutorial, you will be able to:

1. Develop a RESTful API with Python and FastAPI
2. Scaffold a React project with Create React App
3. Manage state operations with React Context API and Hooks
4. Create and render React components in the browser
5. Connect a React application to a FastAPI backend

## What is FastAPI?

FastAPI is a python framework for building fast and efficient backend APIs. It handles both synchronous and asynchronous operations and has built-in support for data validation, authentication, and an interactive documentation powered by OpenAPI.

## What is React?
React is a JavaScript UI library used in building frontend application components. It was developed by Facebook and is currently maintained by Facebook and the open source community.

## Setting up the Project

Start by creating a new folder to hold your project called "fastapi-react":

```sh
$ mkdir fastapi-react
$ cd fastapi-react
```

### Setting up FastAPI

In the "fastapi-react" folder, create a new folder to house the backend:

```sh
$ mkdir backend
$ cd backend
```

Next, create and activate a virtual environment:

```sh
$ python3.9 -m venv venv
$ source venv/bin/activate
$ export PYTHONPATH=$PWD
```

> Feel free to swap out virtualenv and Pip for [Poetry](https://python-poetry.org/) or [Pipenv](https://pipenv.pypa.io/).

Install FastAPI:

```
(venv)$ pip install fastapi==0.61.1 uvicorn==0.11.8
```

[Uvicorn](http://www.uvicorn.org/) is an Asynchronous Server Gateway Interface (ASGI) server that will be responsible for the deployment of our backend API.

Next, create the following files and folders in the "backend" folder:

```sh
└── backend
    ├── main.py
    └── app
        ├── __init__.py
        └── api.py
```

In the *main.py* file, define an entry point for running the application:

```python
import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
```

Here, we instructed the file to run a [Uvicorn](https://www.uvicorn.org/) server on port 8000 and reload on every file change.

Before starting the server via the entry point file, create a base route in *backend/app/api.py*:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}
```

Why do we need [CORSMiddleware](https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware)? In order to make cross-origin requests -- e.g., requests that originate from a different protocol, IP address, domain name, or port -- you need to enable [Cross Origin Resource Sharing](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) (CORS). FastAPI's built-in `CORSMiddleware` handles this for us.

The above setup allows cross-origin requests from our frontend domain and port which at `localhost:3000`.

> For more on the handling of CORS in FastAPI, review the official [docs](https://fastapi.tiangolo.com/tutorial/cors/).


Run the entry point file from your console:

```sh
(venv)$ python main.py
```

Navigate to [http://localhost:8000](http://localhost:8000) in your browser. You should see:

```json
{
  "message": "Welcome to your todo list."
}
```

## Setting up React

Again, we'll be using the [Create React App](https://create-react-app.dev/) CLI tool to scaffold a new React application via [npx](https://nodejs.dev/learn/the-npx-nodejs-package-runner).

Within a new terminal window, navigate to the project directory and then generate a new React application

```sh
$ npx create-react-app frontend
$ cd frontend
```

> If this is your first time scaffolding a React application using the Create React App tool, check out the [documentation](https://create-react-app.dev/docs/getting-started).

To simplify things, remove all files in the "src" folder except the *index.js* file. *index.js* is our base component.

Next, install a UI component library called [Chakra UI](http://chakra-ui.com/):

```sh
$ npm install @chakra-ui/core @emotion/core @emotion/styled emotion-theming
```

After the installation, create a new folder called "components" in the "src" folder, which will be used to hold the application's components, along with two components:

```sh
$ cd src
$ mkdir components
$ cd components
$ touch {Header,Todos}.jsx
```

We'll start with the `Header` component in the *Header.jsx* file:

```jsx
import React from "react";
import { Heading, Flex, Divider } from "@chakra-ui/core";

const Header = () => {
  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      padding="0.5rem"
      bg="gray.400"
    >
      <Flex align="center" mr={5}>
        <Heading as="h1" size="sm">Todos</Heading>
        <Divider />
      </Flex>
    </Flex>
  );
};

export default Header;
```

After importing React and the [Heading](https://chakra-ui.com/heading), [Flex](https://chakra-ui.com/flex), and [Divider](https://chakra-ui.com/divider) components from Chakra UI,we defined a component to render a basic header. The component is then exported for use in the base component.

Next, let's rewrite the base component. Replace the previous code with:

```jsx
import React from "react";
import { render } from 'react-dom';
import { ThemeProvider } from "@chakra-ui/core";

import Header from "./components/Header";

function App() {
  return (
    <ThemeProvider>
      <Header />
    </ThemeProvider>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)
```

[ThemeProvider](https://chakra-ui.com/theme), imported from the Chakra UI library, serves as the parent component for other components using Chakra UI. It provides a theme to all child components (`Header` in this case) via React's [Context API](https://reactjs.org/docs/context.html).

Start your react application from the terminal:

```sh
$ npm run start
```

This will open the React application in your default browser at [http://localhost:3000/](http://localhost:3000/). You should see:

![Todo app](https://res.cloudinary.com/adeshina/image/upload/v1603073365/ylxqc6colgefc5visq3y.png)

## What Are We Building?

For the remainder of this tutorial, you'll be building a todo application where we can perform CRUD operations. By the end, your application will be look like this:

![Todo app](https://res.cloudinary.com/adeshina/image/upload/v1603073714/j7toccssbwjtvma3sk1m.gif)

## GET Route

### Backend

Start by adding a list of todos to *backend/app/api.py*:

```python
todos = [
    {
        "id": "1",
        "item": "Read a book."
    },
    {
        "id": "2",
        "item": "Cycle around town."
    }
]
```

> The todos array above is just dummy data used for the course of this tutorial. The data in the todo object simply represents the structure of individual todos.

Then, add the route handler:

```python
@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return { "data": todos }
```

Manually test the new route at [http://localhost:8000/todo](http://localhost:8000/todo). Check out the interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs) as well:

![Todos](https://res.cloudinary.com/adeshina/image/upload/v1603073619/gzlxusvdnwqnqxygxmqe.png)

### Frontend

In the *Todos.jsx* component, start by importing React, the `useState()` and `useEffect()` hooks, and some Chakra UI components:

```js
import React, {useEffect, useState} from "react";
import {
    Box,
    Button,
    Flex,
    Input,
    InputGroup,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Stack,
    Text,
    useDisclosure
} from "@chakra-ui/core";
```

The `useState` hook is responsible for managing our application's local state while the `useEffect` hook allows us to perform operations such as data fetching.

> For more on React Hooks, review the [Primer on React Hooks](https://testdriven.io/blog/react-hooks-primer/) tutorial and [Introducing Hooks](https://reactjs.org/docs/hooks-intro.html) from the official docs.

Next, create a context for managing global state activities across all components:

```javascript
const TodosContext = React.createContext({
  todos: [], fetchTodos: () => {}
})
```

In the code block above, we defined a context object via [createContext](https://reactjs.org/docs/context.html#reactcreatecontext) that takes in two provider values: `todos` and `fetchTodos`. The `fecthTodos` function will be defined in the next code block.

> Want to learn more about managing state with the React Context API? Check out the [React Context API: Managing State with Ease](https://auth0.com/blog/react-context-api-managing-state-with-ease/) article.

Next, add the `Todos` component:

```javascript
export default function Todos() {
  const [todos, setTodos] = useState([])
  const fetchTodos = async () => {
    const response = await fetch("http://localhost:8000/todo")
    const todos = await response.json()
    setTodos(todos.data)
  }
}
```

Here, we created an empty state variable array, `todos`, and a state method, `setTodos`, so we can update the state variable. Next, we defined a function called `fetchTodos` to retrieve todos from the backend asynchronously and update the `todo` state variable at the end of the function.

Next, within `Todos()`, retrieve the todos using the `fetchTodos` function and render the data by iterating through the todos state variable:

```javascript
useEffect(() => {
  fetchTodos()
}, [])

return (
  <TodosContext.Provider value={{todos, fetchTodos}}>
    <Stack spacing={5}>
      {todos.map((todo) => (
        <b>{todo.item}</b>
      ))}
    </Stack>
  </TodosContext.Provider>
)
```

*Todos.jsx* should now look like:

```jsx
import React, {useEffect, useState} from "react";
import {
    Box,
    Button,
    Flex,
    Input,
    InputGroup,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Stack,
    Text,
    useDisclosure
} from "@chakra-ui/core";

const TodosContext = React.createContext({
  todos: [], fetchTodos: () => {}
})

export default function Todos() {
  const [todos, setTodos] = useState([])
  const fetchTodos = async () => {
    const response = await fetch("http://localhost:8000/todo")
    const todos = await response.json()
    setTodos(todos.data)
  }
  useEffect(() => {
    fetchTodos()
  }, [])
  return (
    <TodosContext.Provider value={{todos, fetchTodos}}>
      <Stack spacing={5}>
        {todos.map((todo) => (
          <b>{todo.item}</b>
        ))}
      </Stack>
    </TodosContext.Provider>
  )
}
```

Import the `Todos` component in *index.js* file and render it:

```jsx
import React from "react";
import { render } from 'react-dom';
import { ThemeProvider } from "@chakra-ui/core";

import Header from "./components/Header";
import Todos from "./components/Todos";  // new

function App() {
  return (
    <ThemeProvider>
      <Header />
      <Todos />  {/* new */}
    </ThemeProvider>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)
```

You app at [http://localhost:3000](http://localhost:3000) should now look like this:

![Client](https://res.cloudinary.com/adeshina/image/upload/v1603073753/eaua7f8ullkth6titjsw.png)

Try adding a new todo to the `todos` list in *backend/app/api.py*. Refresh the browser. You should see the new todo. With that, we're done wth the GET request for retrieving all todos.

## POST Route

### Backend

Start by adding a new route handler to handle POST requests for adding a new todo to *backend/app/api.py*:

```python
@app.post("/todo", tags=["todos"])
async def add_todo(todo: dict) -> dict:
    todos.append(todo)
    return {
        "data": { "Todo added." }
    }
```

With the backend running, you can test the POST route in a new terminal tab using `curl`:

```sh
$ curl -X POST http://localhost:8000/todo -d \
    '{"id": "3", "item": "Buy some testdriven courses."}' \
    -H 'Content-Type: application/json'
```

You should see:

```json
{
    "data: [
        "Todo added."
    ]"
}
```

You should also see the new todo in the response from the [http://localhost:8000/todo](http://localhost:8000/todo) endpoint as well as at [http://localhost:3000/](http://localhost:3000/).

> As an exercise, implement a check to prevent adding duplicate todo items.

### Frontend

Start by adding the shell for adding a new todo *frontend/src/components/Todos.jsx*:

```javascript
function AddTodo() {
  const [item, setItem] = React.useState("")
  const {todos, fetchTodos} = React.useContext(TodosContext)
}
```

Here, we created a new state variable that will hold the value from the form. We also retrieved the context values, `todos` and `fetchTodos()`.

Next, add the functions for obtaining the input from the form and handling the form submission to `AddTodo`:

```javascript
const handleInput = event  => {
  setItem(event.target.value)
}

const handleSubmit = (event) => {
  const newTodo = {
    "id": todos.length + 1,
    "item": item
  }

  fetch("http://localhost:8000/todo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newTodo)
  }).then(fetchTodos)
}
```

In the `handleSubmit` function, we added a POST request and sent data to to the server with the todo info. We then called `fetchTodos` to update `todos`.

Just after the `handleSubmit` function, return the form to be rendered:

```jsx
return (
  <form onSubmit={handleSubmit}>
    <InputGroup size="md">
      <Input
        pr="4.5rem"
        type="text"
        placeholder="Add a todo item"
        aria-label="Add a todo item"
        onChange={handleInput}
      />
    </InputGroup>
  </form>
)
```

In the code block above, we set the form `onSubmit` event listener to the `handleSubmit` function that we created earlier. The todo item value is also updated as the input value changes via the `onChange` listener.

The full `AddTodo` component should now look like:

```jsx
function AddTodo() {
  const [item, setItem] = React.useState("")
  const {todos, fetchTodos} = React.useContext(TodosContext)

  const handleInput = event  => {
    setItem(event.target.value)
  }

  const handleSubmit = (event) => {
    const newTodo = {
      "id": todos.length + 1,
      "item": item
    }

    fetch("http://localhost:8000/todo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newTodo)
    }).then(fetchTodos)
  }

  return (
    <form onSubmit={handleSubmit}>
      <InputGroup size="md">
        <Input
          pr="4.5rem"
          type="text"
          placeholder="Add a todo item"
          aria-label="Add a todo item"
          onChange={handleInput}
        />
      </InputGroup>
    </form>
  )
}
```

Next, add the `AddTodo` component to the `Todos` component like so:

```jsx
export default function Todos() {
  const [todos, setTodos] = useState([])
  const fetchTodos = async () => {
    const response = await fetch("http://localhost:8000/todo")
    const todos = await response.json()
    setTodos(todos.data)
  }
  useEffect(() => {
    fetchTodos()
  }, [])
  return (
    <TodosContext.Provider value={{todos, fetchTodos}}>
      <AddTodo />  {/* new */}
      <Stack spacing={5}>
        {todos.map((todo) => (
          <b>{todo.item}</b>
        ))}
      </Stack>
    </TodosContext.Provider>
  )
}
```

The frontend application should look like this:

![add todo](https://res.cloudinary.com/adeshina/image/upload/v1603073791/juz80sk17pcpixivghgw.png)

Test the form by adding a todo:

![add todo in action](https://res.cloudinary.com/adeshina/image/upload/v1603073813/vvqmclebauev4bq1ntxn.gif)

## PUT Route

### Backend

Add an update route:

```python
@app.put("/todo/{id}", tags=["todos"])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todo["item"] = body["item"]
            return {
                "data": f"Todo with id {id} has been updated."
            }

    return {
        "data": f"Todo with id {id} not found."
    }
```

So, we checked for the todo with an ID matching the one supplied and then, if found, updated the todo's item with the value from the request body.

### Frontend

Start by defining the component `UpdateTodo` in *frontend/src/components/Todos.jsx* and passing two prop values, `item` and `id` to it:

```javascript
function UpdateTodo({item, id}) {
    const {isOpen, onOpen, onClose} = useDisclosure()
    const [todo, setTodo] = useState(item)
    const {fetchTodos} = React.useContext(TodosContext)
}
```

The state variables above are for the modal which will be created later on and to hold the todo value to be updated. The `fetchTodos` context value is also imported for updating `todos` after the changes have been made.

Now, let's write the function responsible for sending PUT requests. In the `UpdateTodo` component body, just after the state and context variables, write:

```javascript
const updateTodo = async () => {
  await fetch(`http://localhost:8000/todo/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ item: todo })
  })
  onClose()
  await fetchTodos()
}
```

In the asynchronous function above, we send a PUT request to the backend and then call the `onClose()` method to close the modal. `fetchTodos()` is then invoked.

Next, render the modal:

```jsx
return (
  <>
    <Button h="1.5rem" size="sm" onClick={onOpen}>Update Todo</Button>
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay/>
      <ModalContent>
        <ModalHeader>Update Todo</ModalHeader>
        <ModalCloseButton/>
        <ModalBody>
          <InputGroup size="md">
            <Input
              pr="4.5rem"
              type="text"
              placeholder="Add a todo item"
              aria-label="Add a todo item"
              value={todo}
              onChange={event => setTodo(event.target.value)}
            />
          </InputGroup>
        </ModalBody>

        <ModalFooter>
          <Button h="1.5rem" size="sm" onClick={updateTodo}>Update Todo</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  </>
)
```

In the above code, we created a modal using Chakra UI's [Modal](https://chakra-ui.com/modal) components. In the modal body, we listened for changes to the textbox and updated the state object, `todo`. Lastly, when the button "Update Todo" is clicked, the function `updateTodo()` is invoked and our todo is updated.

The full component should now look like:

```jsx
function UpdateTodo({item, id}) {
  const {isOpen, onOpen, onClose} = useDisclosure()
  const [todo, setTodo] = useState(item)
  const {fetchTodos} = React.useContext(TodosContext)

  const updateTodo = async () => {
    await fetch(`http://localhost:8000/todo/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ item: todo })
    })
    onClose()
    await fetchTodos()
  }

  return (
    <>
      <Button h="1.5rem" size="sm" onClick={onOpen}>Update Todo</Button>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay/>
        <ModalContent>
          <ModalHeader>Update Todo</ModalHeader>
          <ModalCloseButton/>
          <ModalBody>
            <InputGroup size="md">
              <Input
                pr="4.5rem"
                type="text"
                placeholder="Add a todo item"
                aria-label="Add a todo item"
                value={todo}
                onChange={e => setTodo(e.target.value)}
              />
            </InputGroup>
          </ModalBody>

          <ModalFooter>
            <Button h="1.5rem" size="sm" onClick={updateTodo}>Update Todo</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  )
}
```

Before adding the component to the `Todos` component, we need to add a helper component for rendering todos:

```jsx
function TodoHelper({item, id, fetchTodos}) {
  return (
    <Box p={1} shadow="sm">
      <Flex justify="space-between">
        <Text mt={4} as="div">
          {item}
          <Flex align="end">
            <UpdateTodo item={item} id={id} fetchTodos={fetchTodos}/>
          </Flex>
        </Text>
      </Flex>
    </Box>
  )
}
```

In the component above, we rendered the todo passed to the component and attached an update button to it.

Replace the code in the `return` block within the `Todos` component:

```jsx
return (
  <TodosContext.Provider value={{todos, fetchTodos}}>
    <AddTodo />
    <Stack spacing={5}>
      {
        todos.map((todo) => (
          <TodoHelper item={todo.item} id={todo.id} fetchTodos={fetchTodos} />
        ))
      }
    </Stack>
  </TodosContext.Provider>
)
```

The browser should have a refreshed look:

![todo listing fixed](https://res.cloudinary.com/adeshina/image/upload/v1603073892/kl1ggovegdhpv2tkzqob.png)

Verify that it works:

![Update todo in action](https://res.cloudinary.com/adeshina/image/upload/v1603073964/yejidm3ly9k3d4aw8req.gif)

## DELETE Route

### Backend

Finally, add the delete route:

```python
@app.delete("/todo/{id}", tags=["todos"])
async def delete_todo(id: int) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todos.remove(todo)
            return {
                "data": f"Todo with id {id} has been removed."
            }

    return {
        "data": f"Todo with id {id} not found."
    }
```

### Frontend

Let's write a component for deleting a todo, which we'll be used in the `TodoHelper` component:

```jsx
function DeleteTodo({id}) {
  const {fetchTodos} = React.useContext(TodosContext)

  const deleteTodo = async () => {
    await fetch(`http://localhost:8000/todo/${id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: { "id": id }
    })
    await fetchTodos()
  }

  return (
    <Button h="1.5rem" size="sm" onClick={deleteTodo}>Delete Todo</Button>
  )
}
```

here, we started by invoking the `fetchTodos` function from the global state object. Next, we created an asynchronous function that sends a DELETE request to the server and then updates the list of todos by, again, calling `fetchTodos`. Lastly, we rendered a button that when clicked, triggers `deleteTodo()`.

Next, add the `DeleteTodo` component to the `TodoHelper`:

```jsx
function TodoHelper({item, id, fetchTodos}) {
  return (
    <Box p={1} shadow="sm">
      <Flex justify="space-between">
        <Text mt={4} as="div">
          {item}
          <Flex align="end">
            <UpdateTodo item={item} id={id} fetchTodos={fetchTodos}/>
            <DeleteTodo id={id} fetchTodos={fetchTodos}/>  {/* new */}
          </Flex>
        </Text>
      </Flex>
    </Box>
  )
}
```

The client application should be updated automatically:

![delete button](https://res.cloudinary.com/adeshina/image/upload/v1603074009/ttjc3alkuxgn4mbpq9hv.png)

Now, test the delete button:

![Delete button in action](https://res.cloudinary.com/adeshina/image/upload/v1603074066/qvefu3lmxeqmobzclfyy.gif)

## Conclusion

This post covered the basics of setting up a CRUD application with React and FastAPI.

Check your understanding by reviewing the objectives from the beginning of this post. You can find the source code in the [fastapi-react](https://github.com/github.com/testdrivenio/fastapi-react). Thanks for reading.


Next steps:
1. Deploy the React app to Netlify using this [guide](https://www.netlify.com/blog/2016/07/22/deploy-react-apps-in-less-than-30-seconds/) and update the CORS object in the backend.
2. Deploy the backend API server to Heroku ( feel free to host it on a platform of your choice) and replace the connection URL on the frontend.
3. Set up unit and integration tests with Pytest for the backend and Jest for the frontend.
