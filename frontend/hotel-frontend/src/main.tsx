import "./index.css";
import { createRoot } from "react-dom/client";
import App from "./App";
import { Provider } from "react-redux";
import store from "./store";
import { RouterProvider, useRoutes } from "react-router-dom";
import routes from "./routes";

const root = createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <RouterProvider routes={routes} />
    </Provider>
  </React.StrictMode>
);