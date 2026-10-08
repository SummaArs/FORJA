import { createOonTheme, oonDefaultTheme } from "@oondemand/oon-core-front/theme";

export const theme = createOonTheme({
  id: "ooncore-acme",
  label: "Ooncore Acme",
  extends: oonDefaultTheme,
  density: "comfortable",
});
