## Developing a Single Page App with FastAPI and React

In this tutorial, you'll be building a CRUD todo application with [FastAPI](https://fastapi.tiangolo.com/) and [React](https://reactjs.org/). We'll start by scaffolding a new React application with the `create-react-app` cli and then move on to building the backend RESTful API with FastAPI.

*Final app*:

![todo application](https://res.cloudinary.com/adeshina/image/upload/v1603073714/j7toccssbwjtvma3sk1m.gif)

*Dependencies:*

- React v16.13.1
- create-react-app v3.4.1
- Node v12.1.0
- npm v6.14.0
- npx v6.14.8
- FastAPI v0.61.1
- Python v3.8

## Objectives

By the end of this tutorial, you will be able to:

1. Develop a RESTful API with Python and FastAPI
2. Scaffold a React project using create-react-app
3. Create and render React components in the browser
4. Connect a React application to a FastAPI backend

Before we begin, I assume that you have a basic understanding of React otherwise, go through the [step-by-step guide](https://reactjs.org/docs/hello-world.html) before moving on.

## What is FastAPI?

FastAPI is a modern, high-performance, batteries-included Python web framework that's perfect for building RESTful APIs. It can handle both synchronous and asynchronous requests and has built-in support for data validation, JSON serialization, authentication and authorization, and OpenAPI.

## What is React?

React is an open-source, front end, JavaScript library for building user interfaces or UI components. It is maintained by Facebook and a community of individual developers and companies. React can be used as a base in the development of single-page or mobile applications.

## Setting up the Project

Start by creating a new folder to hold your project called "fastapi-react":

```sh
$ mkdir fastapi-react
$ cd fastapi-react
```

### Setting up FastAPI

In the `fastapi-react` folder, create a new folder to house the backend:

```sh
$ mkdir backend
$ cd backend
```

Next, create and activate a virtual environment:
```sh
$ python3.8 -m venv venv
$ source venv/bin/activate
$ export PYTHONPATH=$PWD
```

> Feel free to swap out virtualenv and Pip for Poetry or Pipenv.

Install FastAPI:

```
(venv)$ pip3 install fastapi==0.61.1 uvicorn==0.11.8
```


Next, create the following files and folders:

```sh
├── backend
│   ├── main.py
│   └── app
│       ├── __init__.py
│       ├── api.py
```

In the *main.py* file, define an entry point for running the application:

```py
import uvicorn

if __name__ == '__main__':
    uvicorn.run('app.api:app', host='0.0.0.0', port=8000, reload=True)
```

Here, we instructed the file to run a [Uvicorn](https://www.uvicorn.org/) server on port 8000 and reload on every file change.

Before starting the server via the entry point file, create a base route in *app/api.py*:

```py
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

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Welcome to your to-do list."}

```

Why do we need CORSMiddleware? In order to make cross-origin requests -- e.g., requests that originate from a different protocol, IP address, domain name, or port -- you need to enable [Cross Origin Resource Sharing](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) (CORS). FastAPI's inbuilt CORSMiddleware handles this for us.

> It's worth noting that the above setup allows cross-origin requests on *all* routes from our frontend domain and port which defaults at `localhost:3000`. In a production environment, you should *only* allow cross-origin resources from where the frontend application is hosted. There is a section about CORS on [FastAPI](https://fastapi.tiangolo.com/tutorial/cors/).


Run the entry point file from your console:

```sh
(venv)$ python main.py
```

Navigate to [http://localhost:8000](http://localhost:8000) in your browser. You should see:

```json
{
  "message": "Welcome to your to-do list."
}
```

Next, create another terminal window and navigate into the project directory where we'll be setting React:

```sh
$ cd fastapi-react
```

## Setting up React

We'll be using the [Create React App CLI tool]() to scaffold a new React application via `npx`.

Generate a new React application

```sh
$ npx create-react-app frontend
$ cd frontend
```

> If this is your first time scaffolding a React application using the Create React App tool, check out the [documentation](https://create-react-app.dev/docs/).

We are more interested in the contents of the `src` folder:

```
├── App.css
├── App.js
├── App.test.js
├── index.css
├── index.js
├── logo.svg
├── setupTests.js
├── serviceWorker.js
```

However, we do not need a couple of these files. So, delete the following files: App.css, App.js, App.test.js, index.css, logo.svg, setupTests.js and serviceWorker.js.

Next, let's install a CSS library, [Chakra UI](http://chakra-ui.com/), to the application:

```
$ npm install @chakra-ui/core @emotion/core @emotion/styled emotion-theming
```

After the installation, create folder **Components** that'll hold the header and Todo component:

```
$ mkdir Components
$ cd Components
$ touch {Header,Todos}.jsx
```

Let's write the Header component in the `Header.jsx` file:

Begin by importing React from the "react" library, Heading, Flex and Divider components from chakra-UI:

```js
import React from "react";
import {Heading, Flex, Divider} from "@chakra-ui/core";
```

Next, define the component:

```js
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
                <Heading as="h1" size="sm">
                    Todos
                </Heading>
                <Divider />
            </Flex>
        </Flex>
    );
};

export default Header;
```

In the component above, we defined a component to render a header using Chakra UI's *Flex* and *Heading* component. The component is then exported for use in the base component located in `src/index.js`.

Next, let's rewrite the base component located in `src/index.js`:

Start by deleting the previous code, then import React and ReactDOM's render function:

```js
import React from "react";
import {render} from 'react-dom';
```

Next, import Chakra UI theme's `ThemeProvider` and the `Header` component:

```js
import { ThemeProvider } from "@chakra-ui/core";
import Header from "./Components/Header";
```

The `ThemeProvider` imported from the Chakra UI library serves as the parent component for other components using Chakra UI. The `ThemeProvider` enables the library's context API interacts with the component's using fragments of Chakra UI. We will learn more about the context API when we use it in the todo component in the later section of this article.

> Read further on the Context API: [Introduction to React Context API](https://www.smashingmagazine.com/2020/01/introduction-react-context-api/).

Next, write the application's base component:

```js
function App() {
    return (
        <ThemeProvider>
            <Header />
        </ThemeProvider>
    )
}
```

In the component above, we're returning the `Header` component as an object of `ThemeProvider`. Render the component next:

```
const rootElement = document.getElementById("root")
render(<App />, rootElement)
```

In the code block above, we created a variable `rootElement` to point to a document node with the ID "root" then render the component on the `rootElement's` node.

Start your react application from the terminal:

```sh
$ npm run start
```

The command above automatically open the React application in your browser, the todo app looks like this:

![Todo app](https://res.cloudinary.com/adeshina/image/upload/v1603073365/ylxqc6colgefc5visq3y.png)


## What we will be building

For the course of this tutorial, we will be building a todo application where we can perform CRUD operations. By the end of this tutorial, our application will be functioning like this:

![Todo app](https://res.cloudinary.com/adeshina/image/upload/v1603073714/j7toccssbwjtvma3sk1m.gif)

> In the next couple of sections, the backend will be referred to as **Server** and the frontend **Client**.

## GET Route

### Server

Start by adding a list of todos to *app/api.py*:

```py
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

Add the route handler:


```py
@app.get("/todo", tags=["To-dos"])
async def get_todos() -> dict:
    return {
        "data": todos
    }

```

Manually test the new route at [http://localhost:8000/todo](http://localhost:8000/todo). You can also test it at the interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs):

![Todos](https://res.cloudinary.com/adeshina/image/upload/v1603073619/gzlxusvdnwqnqxygxmqe.png)

### Client

In the `Todos.jsx` file, start by importing React, the `useState()`, `useEffect()` hook and some chakra components:

```js
import React, {useEffect, useState} from 'react';
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

> You can read more on [State Hook](https://reactjs.org/docs/hooks-state.html) and [Effect Hook](https://reactjs.org/docs/hooks-effect.html).


Next, create a context for managing global state activities in all components:

```js
const TodosContext = React.createContext({
    todos: [], fetchTodos: () => {
    }
})
```

In the code block above, we define a context object that takes in two provider values, **todos** and **fetchTodos**. The `fecthTodos()` function will be defined in the next code block.

> Here's an article on managing state with React Context API : [React Context API: Managing State with Ease](https://auth0.com/blog/react-context-api-managing-state-with-ease/)


Next, write the todo component:

```js
export default function Todos(){
    const [todos, setTodos] = useState([])
    const fetchTodos = async () => {
        const response = await fetch('http://localhost:8000/todo')
        const todos = await response.json()
        setTodos(todos.data)
    }
}
```

In the code block above, we create an empty state variable array, todos and a state method setTodos to enable us to update the state variable. Next, we define a function `fetchTodos()` to retrieve todos from the backend asynchronously and update the todo state variable at the end of the function.

Next, let's retrieve todos using the `fetchTodos` function and render the data by iterating through the todos state variable:

```js
useEffect(() => {
    fetchTodos()
}, [])

return (
    <TodosContext.Provider value={{todos, fetchTodos}}>
        <Stack spacing={5}>
            {todos.map((todo) => (
                <b>{todo.item}</b>
            )) }
        </Stack>
    </TodosContext.Provider>
)
```

Next, import the todo component in `index.js` file and render it:


```js
import Todos from './Components/Todos';

function App(){
    return (
        <ThemeProvider>
            ...
            <Todos />
        </ThemeProvider>
    )
}
```

The todo app at [http://localhost:3000](http://localhost:3000) displays:


![Client](https://res.cloudinary.com/adeshina/image/upload/v1603073753/eaua7f8ullkth6titjsw.png)

## POST Route

### Server

Let's add the route handler to hanled POST requests for adding a new book:

```py
@app.post("/todo", tags=["To-dos"])
async def add_todo(todo: dict) -> dict:
    todos.append(todo)
    return {
        "data": {
            "To-do added."
        }
    }
```

With the backend running, you can test the POST route in a new terminal tab using curl:

```sh
$ curl -X POST http://localhost:8000/todo -d \
    '{"id": "3", "item": "Buy some testdriven course."}' \
    -H 'Content-Type: application/json'
```

You should see:

```json
{
    "data: [
        "To-do added."
    ]"
}
```

You should also see the new todo in the response from [http://localhost:8000/todo](http://localhost:8000/todo) endpoint.

> As an exercise, implement a check to prevent adding duplicate todo items.

### Client

Before we write the component for adding todo, 

```
function AddTodo() {
    const [item, setItem] = React.useState("")
    const {todos, fetchTodos} = React.useContext(TodosContext)
}
```

We started by creating a state variable that'll hold the value from the `input` field. We also retrieved our context values, `todos` and `fetchTodos()`.

Next, write the methods that'll handle input and submission in the component:

```js
const handleInput = e  => {
    setItem(e.target.value)
}

const handleSubmit = (e) => {
    const newTodo = {
        "id": todos.length + 1,
        "item": item
    }

    fetch('http://localhost:8000/todo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newTodo)
    }).then(fetchTodos)
}
```

In the `handleSubmit` method, we send a POST request to the server containing the new todo value and update the list of todos by calling `fetchTodos` at the end of the fetch call. Just after the `handleSubmit` method, return the form to be rendered:

```js
return (
    <form onSubmit={handleSubmit}>
            <InputGroup size="md">
                <Input
                    pr='4.5rem'
                    type="text"
                    placeholder="Add a todo item"
                    aria-label="Add a todo item"
                    onChange={handleInput}
                />
            </InputGroup>
        </form>
)
```

In the code block above, we set the form `onSubmit` event listener to the `handleSubmit` function we created earlier. The todo item value is also updated as the input value changes; this is effected by the `onChange` listener.

Next, add the `AddTodo` component to the `Todos` component such that the return block is the same as:

```js
<TodosContext.Provider value={{todos, fetchTodos}}>
            <AddTodo />
            <Stack spacing={5}>
                {
                    todos.map((todo) => (
                        <b>{todo.item}</b>
                    ))
                }
            </Stack>
        </TodosContext.Provider>
```

The client application should look like this:

![add todo](https://res.cloudinary.com/adeshina/image/upload/v1603073791/juz80sk17pcpixivghgw.png)

Go on, test the input by adding a todo.

![add todo in action](https://res.cloudinary.com/adeshina/image/upload/v1603073813/vvqmclebauev4bq1ntxn.gif)


## PUT Route

### Server

We'll start by adding an update route:

```py
@app.put("/todo/{id}", tags=["To-dos"])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if todo['id'] == id:
            todo['item'] = body['item']

    return {
        "data": "Todo with id {} has been updated.".format(id)
    }
```

In the code block above, we check for the todo with an id matching the one supplied and then update the todo's item with the value from the request body.


### Client

Start by defining the component `UpdateTodo` and pass two prop values, *item* and *id*:

```js
function UpdateTodo({item, id}) {
    const {isOpen, onOpen, onClose} = useDisclosure()
    const [todo, setTodo] = useState(item)
    const {fetchTodos} = React.useContext(TodosContext)
}
```

The state variables above are for the modal which will be created later on and to hold the todo value to be updated. The `fetchTodos` context value is also imported for reflecting the changes made. Next, let's write the function responsible for sending PUT requests:

In the component body just after the state and context variables, write:

```js
const updateTodo = async () => {
    await fetch(`http://localhost:8000/todo/{id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            item: todo
        })
    })
    onClose()
    await fetchTodos()
}
```

In the asynchronous function above, we send a PUT request to the backend and then call the `onClose()` method to close the modal after which we invoke `fetchTodos()` to update our todo list. Next, render the modal:

```js
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
                            pr='4.5rem'
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
```

In the code block above, we created a modal using [Chakra UI's Modal components](https://chakra-ui.com/modal). In the modal body, we listen to changes in the textbox and effect the changes to the state object, todo. Lastly, when the button "Update Todo" is clicked, the function `updateTodo()` is invoked and our todo is updated.

However, we need to update the `Todos` render method. To do that, we'll create a helper component for rendering todos:

```js
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

In the component above, we render the todo passed to the component and attach the update button. Let's refactor the `Todos` component to effect this change:

Replace the code in the `return` block to:

```js
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
```

The browser should have a refreshed look:

![todo listing fixed](https://res.cloudinary.com/adeshina/image/upload/v1603073892/kl1ggovegdhpv2tkzqob.png)

Verify that it works:

![Update todo in action](https://res.cloudinary.com/adeshina/image/upload/v1603073964/yejidm3ly9k3d4aw8req.gif)

## DELETE Route

### Server

Add the delete route method:

```py
@app.delete("/todo/{id}", tags=["To-dos"])
async def delete_todo(id: int) -> dict:
    for todo in todos:
        if todo['id'] == id:
            todos.remove(todo)
    return {
        "data": "To-do with id {} removed.".format(id)
    }

```


### Client

Let's write a component for deleting a todo. This component will be used in the `TodoHelper` component:


```js
function DeleteTodo({id}) {
    const {fetchTodos} = React.useContext(TodosContext)

    const deleteTodo = async () => {
        await fetch(`http://localhost:8000/todo/{id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: {
                "id": id
            }
        })
        await fetchTodos()
    }
    return (
        <Button h="1.5rem" size="sm" onClick={deleteTodo}>Delete Todo</Button>
    )
}
```

In the code block above, we start by invoking the `fetchTodos()` method from the global state object. Next, we create an asynchronous function that sends a DELETE request to the server and then updates the list of todos by invoking `fetchTodos()`. Lastly, we render a button which when clicked, triggers `deleteTodo()`.

Next, add the `DeleteTodo` component to the `TodoHelper`:

```js
<Box p={1} shadow="sm">
            <Flex justify="space-between">
                <Text mt={4} as="div">
                    {item}
                    <Flex align="end">
                        <UpdateTodo item={item} id={id} fetchTodos={fetchTodos}/>
                        <DeleteTodo id={id} fetchTodos={fetchTodos}/>
                    </Flex>
                </Text>
            </Flex>
        </Box>
```

The client application should be updated automatically:

![delete button](https://res.cloudinary.com/adeshina/image/upload/v1603074009/ttjc3alkuxgn4mbpq9hv.png)

Now, test the delete button:

![Delete button in actino](https://res.cloudinary.com/adeshina/image/upload/v1603074066/qvefu3lmxeqmobzclfyy.gif)

## Conclusion

This post covered the basics of setting up a CRUD application with React and FastAPI.

Check your understanding by reviewing the objectives from the beginning of this post You can find the source code in the [fastapi-react](https://github.com/github.com/testdrivenio/fastapi-react). Thanks for reading.
