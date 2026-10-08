import { defineOonRoutes } from "@oondemand/oon-core-front/routing";
import { HomePage } from "../pages/HomePage";

export const routes = defineOonRoutes([
  { path: "/", component: HomePage },
]);
