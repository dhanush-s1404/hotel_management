import { createRoutes } from "react-router-dom";
import { Lazy } from "react";
import Loading from "../components/Loading";

const Login = Lazy(() => import("../components/Login"));
const Dashboard = Lazy(() => import("../components/Dashboard"));
const Rooms = Lazy(() => import("../components/rooms/Index"));
const RoomsNew = Lazy(() => import("../components/rooms/New"));
const RoomsShow = Lazy(() => import("../components/rooms/Show"));
const Customers = Lazy(() => import("../components/customers/Index"));
const CustomersNew = Lazy(() => import("../components/customers/New"));
const CustomersShow = Lazy(() => import("../components/customers/Show"));
const Bookings = Lazy(() => import("../components/bookings/Index"));
const BookingsNew = Lazy(() => import("../components/bookings/New"));
const BookingsShow = Lazy(() => import("../components/bookings/Show"));
const Payments = Lazy(() => import("../components/payments/Index"));
const Reports = Lazy(() => import("../components/reports/Reports"));

export default createRoutes(() => [
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/",
    element: <Dashboard />,
    children: [
      {
        path: "rooms",
        element: <Rooms />,
      },
      {
        path: "rooms/new",
        element: <RoomsNew />,
      },
      {
        path: "rooms/:id",
        element: <RoomsShow />,
      },
      {
        path: "customers",
        element: <Customers />,
      },
      {
        path: "customers/new",
        element: <CustomersNew />,
      },
      {
        path: "customers/:id",
        element: <CustomersShow />,
      },
      {
        path: "bookings",
        element: <Bookings />,
      },
      {
        path: "bookings/new",
        element: <BookingsNew />,
      },
      {
        path: "bookings/:id",
        element: <BookingsShow />,
      },
      {
        path: "payments",
        element: <Payments />,
      },
      {
        path: "reports",
        element: <Reports />,
      },
    ],
  },
]);