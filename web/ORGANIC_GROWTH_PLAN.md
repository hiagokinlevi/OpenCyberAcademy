# OpenCyber Academy: plano de crescimento orgânico

**Linha de base verificada em 19/10/2026.** Meta aspiracional: pelo menos 100.000 sessões de origem orgânica por dia, sustentadas por 30 dias. Sessão, clique de busca, pessoa, visualização de página e conta de aluno são medidas diferentes. Não há hoje uma fonte completa e validada para sessões orgânicas totais; a meta só será declarada atingida depois de instrumentação e reconciliação entre Search Console, GA4 consentido e contagem agregada de acessos sem bots.

## Ponto de partida

| Fonte | Período e resultado | Limite de interpretação |
| --- | --- | --- |
| [Google Search Console: desempenho](https://search.google.com/search-console/performance/search-analytics?resource_id=sc-domain%3Aopencyber.academy) | Relatório de 3 meses; dados disponíveis de 12 a 17/10: **160 impressões, 3 cliques, CTR 1,9%, posição média 23,3** | Cliques do Google, não usuários ou sessões de todos os buscadores. Relatório atualizado com atraso. |
| [Google Search Console: sitemaps](https://search.google.com/search-console/sitemaps?resource_id=sc-domain%3Aopencyber.academy) | Índices EN, PT e ES processados. URLs descobertas: **4.018**, **2.600**, **556**, respectivamente. | Descoberta não comprova indexação. A página de [indexação](https://search.google.com/search-console/index?resource_id=sc-domain%3Aopencyber.academy) ainda mostra “dados em processamento”. |
| [GA4: propriedade OpenCyber Academy](https://analytics.google.com/analytics/web/#/a411968914p558920623/reports/intelligenthome) | Últimos 7 dias: **1 usuário ativo, 130 visualizações** no painel. | Medição depende de consentimento e pode incluir navegação de teste; não representa tráfego total. Search Console ainda não está associado à propriedade. |
| [Atividade pública](https://opencyber.academy/insights/) | Últimos 30 dias: **2 navegadores participantes, 49 visualizações, 8 leituras de 30 s, 3 aberturas de exercícios**; **1 conta de aluno** no total histórico. | Apenas eventos opt-in; navegador não equivale a pessoa. Conta cadastrada não equivale a aluno ativo. |

**Escala da meta:** a CTR hipotética de 4% exigiria cerca de 2,5 milhões de impressões de busca por dia para 100.000 cliques diários. É uma conta de cenário, não uma previsão. O domínio está no início da distribuição orgânica; nenhum prazo curto ou resultado é garantido.

## Medição e decisões

1. **A cada semana:** registrar cliques, impressões, CTR, páginas e consultas do Search Console nos últimos 7 e 28 dias, separados por país, idioma e tipo de página. Usar dias completos e comparar janelas equivalentes. Conferir indexação e motivos de exclusão quando o relatório deixar de processar.
2. **A cada mês:** apurar sessões `Organic Search` por domínio/idioma no GA4 consentido, com a taxa de consentimento apresentada ao lado. Comparar com cliques de busca e estatísticas agregadas do Cloudflare filtradas por bots; investigar discrepâncias antes de publicar um total. Não extrapolar automaticamente opt-in para pessoas únicas.
3. **Aprendizagem:** acompanhar contas, alunos ativos de 7/30 dias, lições realmente lidas, exercícios iniciados/concluídos e retenção na primeira semana. Esses indicadores precisam de definição e consulta agregada próprias antes de serem publicados. Não misturar acesso livre com contas.
4. **Experimento:** cada alteração de página tem hipótese, URLs, data de publicação, revisão do texto, amostra de comparação e avaliação após 28 dias. Contar ganho de cliques e leituras, não somente mais URLs descobertas.

## Execução em fases

### Fase 1: medição e descoberta (0–30 dias)

- Conferir diariamente os três sitemaps processados e amostrar URLs EN/PT/ES por inspeção de URL: resposta 200, conteúdo efetivamente escrito, canonical próprio, idioma, links internos, título e indexabilidade. Corrigir somente falhas comprovadas. Sitemaps incluem apenas ensino publicado; planos não viram aulas indexáveis.
- Quando a cobertura do Search Console estiver disponível, classificar exclusões por causa e por tipo de página. Priorizar canonical errado, redirecionamento, 404, `noindex` indevido e páginas rastreadas sem conteúdo suficiente. Não solicitar indexação em massa de páginas fracas.
- Tornar as páginas de curso úteis por si: escopo, público, pré-requisitos, objetivo **pretendido**, disponibilidade real e links diretos às aulas. Esta primeira melhoria usa o resumo já publicado no README de cada curso inglês e mantém planos separados de aulas escritas.
- Estabelecer painel semanal de aquisição e aprendizado com as definições acima. Vincular GA4 e Search Console apenas após conferir permissões de quem verá os relatórios.

**Gate:** métricas com período e definição reproduzíveis; nenhum número de indexação ou aluno inventado. Meta indicativa: sair de unidades para dezenas de cliques orgânicos diários, condicionada à indexação real.

### Fase 2: profundidade editorial e intenção de busca (31–90 dias)

- Escolher 3–5 tópicos iniciais onde já existe aula inglesa sólida e verificável. Para cada um, mapear dúvidas reais do Search Console, intenção de iniciante e praticante, concorrentes e lacunas de resposta. Atualizar a aula canônica no único `MANUSCRIPT.md`, com conceito, exemplo, exercício, resposta, fontes primárias e próximos passos. Não criar páginas automáticas que repetem o mesmo texto.
- Criar guias de entrada curados que liguem conceitos, cursos, lições e testes **publicados**. Usar URLs permanentes, títulos específicos, HTML legível sem JavaScript e dados estruturados apenas quando correspondem ao conteúdo visível. Medir cliques para a próxima lição e leituras de 30 s.
- Revisar 20 páginas por semana com alto número de impressões e baixo CTR: título, descrição, primeiro parágrafo, alinhamento à consulta e vínculo para a resposta. Verificar no Search Console após 28 dias; não alterar várias variáveis por página sem registro.
- Distribuir conteúdo original em comunidades técnicas, repositórios, currículos abertos e parceiros acadêmicos com contribuição genuína e permissão. Sem compra de links, troca artificial ou postagem em massa.

**Gate:** crescimento de cliques e leituras, cobertura de consultas relevantes e estabilidade de URLs. Meta indicativa: centenas de cliques diários; replanejar se a tendência não aparecer.

### Fase 3: autoridade temática e retenção (meses 4–12)

- Repetir o modelo que provar ganho: coleção coesa de cursos ingleses revisados, hubs temáticos originais e tarefas práticas compartilháveis. Fortalecer citações e links para fontes oficiais, corrigir conteúdo desatualizado e publicar notas de revisão.
- Melhorar a jornada aula → exercício → resultado explicado → próxima aula. Testar compreensão e taxa de continuidade, preservando leitura sem conta. Separar métricas de acesso, estudo e conclusão.
- Buscar referências editoriais de instituições, docentes e mantenedores de material aberto por utilidade real. Publicar recursos que mereçam citação: tabelas de decisão, casos sintéticos reproduzíveis e comparações fundamentadas.
- Traduzir apenas unidades inglesas revistas e pinadas, conforme `BOOK_STANDARD.md`; português antes do espanhol planejado. Não publicar as seis demais línguas antes dos gates.

**Gate:** milhares de sessões orgânicas diárias comprovadas, qualidade editorial e retenção estáveis. Só então calcular previsão para 100.000/dia com base em coortes reais, distribuição por consultas e capacidade operacional.

### Fase 4: expansão para 100.000/dia (após evidência)

- Escalar os tópicos, formatos e idiomas que tiverem demanda comprovada; manter manutenção técnica e editorial por versão. Diversificar Google, Bing e busca em outras plataformas sem contar tráfego social/direto como orgânico de busca.
- Critério de sucesso: média móvel de **100.000 sessões orgânicas/dia por 30 dias**, excluindo bots e tráfego interno, com crescimento de alunos ativos e leitura; publicar fonte, definição, período e limitações. Um pico isolado não basta.

## Regras de qualidade

Não confundir sitemap com indexação, catálogo com livro concluído, plano com aula, cliques com alunos, nem visualizações com pessoas. Evitar páginas fabricadas para consultas, conteúdo repetido entre níveis, dados estruturados enganosos e promessas de credenciamento. Preservar fontes, direitos, acessibilidade, privacidade e ordem editorial do projeto. Publicação do site ocorre apenas pelo procedimento local autorizado; este plano não autoriza GitHub Actions.
