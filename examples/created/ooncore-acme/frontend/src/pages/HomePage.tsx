import { Stack, Text } from "@chakra-ui/react";
import { CorePageHeader, CoreStatusPanel, CoreSummaryCards } from "@oondemand/oon-core-front/ui";

export function HomePage() {
  return (
    <Stack gap={6} p={6}>
      <CorePageHeader
        title="Boas-vindas ao Ooncore Acme"
        description="A fundação técnica está pronta para receber a experiência e o domínio do app."
      />
      <Stack gap={6}>
        <CoreSummaryCards items={[
          { id: "core", label: "OonCore", value: "Pronto", description: "Shell, autenticação, sessão, tenant e RBAC." },
          { id: "platform", label: "Plataforma Oon", value: "Governada", description: "Publicação, ambientes, acesso e proveniência." },
        ]} />
        <CoreStatusPanel
          title="Próximos passos"
          status="Code-first"
          description="Crie páginas em src/pages, componentes em src/components e organize o domínio em src/features."
        />
        <Text color="text.muted">Menus, rotas, layouts e temas ficam em src/app e podem combinar componentes locais com blocos públicos do OonCore.</Text>
      </Stack>
    </Stack>
  );
}
