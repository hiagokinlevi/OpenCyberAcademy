import subjectTitlesData from './subject-titles.json';

type Language = 'en' | 'pt' | 'es';
const subjectTitles = subjectTitlesData as Record<string, { pt: string; es: string }>;

export function siteLanguage(): Language {
  const selected = document.documentElement.dataset.language;
  return selected === 'pt' || selected === 'es' ? selected : 'en';
}

export function editionLanguage(): string {
  const requested = new URLSearchParams(location.search).get('lang');
  return requested && ['en', 'pt', 'es', 'he', 'fr', 'ru', 'de', 'zh', 'ja'].includes(requested) ? requested : siteLanguage();
}

// Interface text only. Course manuscripts and quoted reference documents retain
// the language of their published edition.
const copy: Record<string, [string, string]> = {
  'PUBLIC STUDY ACTIVITY': ['ATIVIDADE PÚBLICA DE ESTUDO', 'ACTIVIDAD PÚBLICA DE ESTUDIO'],
  'Learning in motion': ['O estudo em movimento', 'El aprendizaje en marcha'],
  'Last 30 days · visitors who chose analytics': ['Últimos 30 dias · visitantes que permitiram análise de uso', 'Últimos 30 días · visitantes que permitieron el análisis de uso'],
  'Participating browsers': ['Navegadores participantes', 'Navegadores participantes'],
  'Page views': ['Visualizações de página', 'Visualizaciones de página'],
  'Reading sessions · 30 s visible': ['Sessões de leitura · 30 s visíveis', 'Sesiones de lectura · 30 s visibles'],
  'Exercise opens': ['Aberturas de exercícios', 'Aperturas de ejercicios'],
  'A browser is not necessarily a person.': ['Um navegador não equivale necessariamente a uma pessoa.', 'Un navegador no equivale necesariamente a una persona.'],
  'registered learner accounts · all time. Counts begin when this feature is published and exclude visitors who decline measurement.': ['contas de estudante cadastradas · total histórico. As contagens começam com a publicação deste recurso e excluem visitantes que recusam a medição.', 'cuentas de estudiante registradas · total histórico. Los recuentos empiezan con la publicación de esta función y excluyen a quienes rechazan la medición.'],
  'How counting works': ['Como funciona a contagem', 'Cómo funciona el recuento'],
  'Explore course and page activity →': ['Explorar atividade por curso e página →', 'Explorar actividad por curso y página →'],
  'Public activity': ['Atividade pública', 'Actividad pública'],
  'PUBLIC ACTIVITY': ['ATIVIDADE PÚBLICA', 'ACTIVIDAD PÚBLICA'],
  'See how the library is used.': ['Veja como a biblioteca é usada.', 'Descubre cómo se utiliza la biblioteca.'],
  'Explore visits, visible reading sessions and exercise opens across public courses and pages. These are counts from browsers that allowed measurement, beginning with this feature’s launch.': ['Explore visitas, sessões de leitura visíveis e aberturas de exercícios nos cursos e páginas públicas. São contagens de navegadores que permitiram a medição, desde a publicação deste recurso.', 'Explora visitas, sesiones de lectura visibles y aperturas de ejercicios en cursos y páginas públicas. Son recuentos de navegadores que permitieron la medición, desde el lanzamiento de esta función.'],
  'COURSE ACTIVITY': ['ATIVIDADE DOS CURSOS', 'ACTIVIDAD DE CURSOS'],
  'Courses with activity': ['Cursos com atividade', 'Cursos con actividad'],
  'Views include course entry pages and published lesson pages. A reading session means the lesson remained visible for 30 seconds.': ['As visualizações incluem páginas iniciais de curso e aulas publicadas. Uma sessão de leitura significa que a aula ficou visível por 30 segundos.', 'Las visualizaciones incluyen páginas iniciales de curso y lecciones publicadas. Una sesión de lectura significa que la lección permaneció visible 30 segundos.'],
  'PAGE ACTIVITY': ['ATIVIDADE DAS PÁGINAS', 'ACTIVIDAD DE PÁGINAS'],
  'Most viewed pages': ['Páginas mais visualizadas', 'Páginas más vistas'],
  'These public totals omit visitors who declined analytics and cannot identify individual people.': ['Esses totais públicos excluem visitantes que recusaram a análise de uso e não identificam pessoas.', 'Estos totales públicos excluyen a quienes rechazaron el análisis de uso y no identifican a personas.'],
  'Course': ['Curso', 'Curso'],
  'Views': ['Visualizações', 'Visualizaciones'],
  '30s reads': ['Leituras de 30 s', 'Lecturas de 30 s'],
  'Browsers': ['Navegadores', 'Navegadores'],
  'Page': ['Página', 'Página'],
  'Loading activity…': ['Carregando atividade…', 'Cargando actividad…'],
  'The course and page lists show the twelve most active entries in the last 30 days. One browser can represent multiple people, and one person can use multiple browsers. An opt-in view is counted at most once per browser, page and half-hour.': ['As listas mostram as doze entradas mais ativas nos últimos 30 dias. Um navegador pode representar várias pessoas e uma pessoa pode usar vários navegadores. Cada visualização consentida é contada no máximo uma vez por navegador, página e meia hora.', 'Las listas muestran las doce entradas más activas de los últimos 30 días. Un navegador puede representar a varias personas y una persona puede usar varios navegadores. Cada visita consentida se cuenta como máximo una vez por navegador, página y media hora.'],
  'Read the measurement and privacy details →': ['Ler detalhes da medição e privacidade →', 'Leer detalles de medición y privacidad →'],
  'This page:': ['Esta página:', 'Esta página:'],
  'opt-in views in 30 days': ['visualizações consentidas em 30 dias', 'visualizaciones consentidas en 30 días'],
  'completed test attempts · all time': ['tentativas de teste concluídas · total histórico', 'intentos de prueba completados · total histórico'],
  'Available courses with tests': ['Cursos com testes disponíveis', 'Cursos con pruebas disponibles'],
  'Browse available tests ↓': ['Ver testes disponíveis ↓', 'Ver pruebas disponibles ↓'],
  'Choose language, subject and level manually': ['Escolher idioma, tema e nível manualmente', 'Elegir idioma, tema y nivel manualmente'],
  'Browse by course here, then choose a chapter below. Questions are tied to published teaching and source files.': ['Explore por curso e escolha um capítulo abaixo. As perguntas seguem aulas publicadas e arquivos de origem.', 'Explora por curso y elige un capítulo abajo. Las preguntas se basan en lecciones publicadas y archivos fuente.'],
  'That same permission also enables the Academy’s own public counters. A random browser identifier is created locally after opt-in; only its SHA-256 digest, page path and event type are stored in D1. D1 does not store an IP address, email, query string or browser details with these events. Each page view, exercise open and reading session is counted at most once per browser, page and half-hour. A reading session requires the lesson to remain visible for 30 seconds. Events are removed after 30 days. “Participating browsers” is not a count of people, and public totals exclude visitors who decline measurement.': ['A mesma permissão ativa os contadores públicos da Academy. Um identificador aleatório é criado neste navegador após o consentimento; apenas o hash SHA-256, o caminho da página e o tipo de evento são salvos no D1. O D1 não guarda endereço IP, email, parâmetros da URL nem detalhes do navegador nesses eventos. Cada visualização, abertura de exercício e sessão de leitura é contada no máximo uma vez por navegador, página e meia hora. A sessão exige 30 segundos com a aula visível. Os eventos são removidos após 30 dias. “Navegadores participantes” não é uma contagem de pessoas e exclui visitantes que recusam a medição.', 'El mismo permiso activa los contadores públicos de Academy. Tras el consentimiento se crea un identificador aleatorio en el navegador; en D1 solo se guardan su hash SHA-256, la ruta de la página y el tipo de evento. D1 no guarda direcciones IP, correo, parámetros de URL ni detalles del navegador con estos eventos. Cada visita, apertura de ejercicio y sesión de lectura se cuenta como máximo una vez por navegador, página y media hora. La sesión requiere 30 segundos con la lección visible. Los eventos se eliminan tras 30 días. “Navegadores participantes” no es un recuento de personas y excluye a quienes rechazan la medición.'],
  'Your choice is kept in this browser\'s local storage. You can change it using “Analytics preferences” in the footer. Opting out removes the browser identifier and stops later measurements from this browser; previously recorded Academy events expire after 30 days. Google’s own retention follows its policies. Global Privacy Control and Do Not Track disable both analytics systems here.': ['Sua escolha fica no armazenamento local do navegador e pode ser alterada em “Preferências de analytics” no rodapé. A recusa remove o identificador e interrompe novas medições neste navegador; os eventos anteriores da Academy expiram após 30 dias. A retenção do Google segue as políticas dele. Global Privacy Control e Do Not Track desativam ambos os sistemas aqui.', 'Tu elección se guarda localmente en el navegador y puede cambiarse en “Preferencias de analytics” al pie. Rechazar elimina el identificador y detiene nuevas mediciones en este navegador; los eventos anteriores de Academy vencen en 30 días. La retención de Google sigue sus políticas. Global Privacy Control y Do Not Track desactivan ambos sistemas aquí.'],
  'Tests': ['Testes', 'Pruebas'],
  'Test yourself.': ['Teste você mesmo.', 'Ponte a prueba.'],
  'Test yourself →': ['Teste você mesmo →', 'Ponte a prueba →'],
  'CHAPTER ASSESSMENTS': ['AVALIAÇÕES POR CAPÍTULO', 'EVALUACIONES POR CAPÍTULO'],
  'Choose your language': ['Escolha seu idioma', 'Elige tu idioma'],
  'Choose a subject': ['Escolha um tema', 'Elige un tema'],
  'Choose a level': ['Escolha um nível', 'Elige un nivel'],
  'Published chapter tests': ['Testes publicados por capítulo', 'Pruebas publicadas por capítulo'],
  'Available tests now': ['Testes disponíveis agora', 'Pruebas disponibles ahora'],
  'Only reviewed questions tied to a published chapter appear here. Choose one to open its course assessment.': ['Aqui aparecem apenas perguntas revisadas de capítulos publicados. Escolha uma para abrir a avaliação do curso.', 'Aquí solo aparecen preguntas revisadas de capítulos publicados. Elige una para abrir la evaluación del curso.'],
  'Exercises in the public book': ['Exercícios do livro público', 'Ejercicios del libro público'],
  'Open an authored lesson or chapter to see its exercises. Reviewed five-choice practice questions show the result after a choice; where a question is still being authored, the prompt and worked answer remain available. Timed chapter tests appear separately above.': ['Abra uma aula ou capítulo escrito para ver os exercícios. Questões revisadas com cinco alternativas mostram o resultado após a escolha; quando a questão ainda está sendo escrita, o enunciado e a resposta comentada continuam disponíveis. Os testes cronometrados aparecem separadamente acima.', 'Abre una lección o capítulo redactado para ver los ejercicios. Las preguntas revisadas con cinco opciones muestran el resultado después de elegir; cuando aún se está escribiendo una pregunta, el enunciado y la respuesta desarrollada siguen disponibles. Las pruebas cronometradas aparecen por separado arriba.'],
  'TEN SECONDS PER QUESTION': ['DEZ SEGUNDOS POR PERGUNTA', 'DIEZ SEGUNDOS POR PREGUNTA'],
  'ATTEMPT COMPLETE': ['TENTATIVA CONCLUÍDA', 'INTENTO COMPLETADO'],
  'Try again': ['Tentar novamente', 'Intentarlo de nuevo'],
  'Claim course certificate': ['Solicitar certificado do curso', 'Solicitar certificado del curso'],
  'Choose a published course below, or select a language, subject and level manually. Each chapter test has ten questions, five choices per question and ten seconds for each answer. Reading stays free; saving results requires student sign-in.': ['Escolha um curso com testes publicados abaixo ou selecione idioma, tema e nível manualmente. Cada teste tem dez perguntas, cinco alternativas por pergunta e dez segundos para responder. A leitura continua gratuita; salvar resultados exige cadastro de estudante.', 'Elige un curso con pruebas publicadas abajo o selecciona idioma, tema y nivel manualmente. Cada prueba tiene diez preguntas, cinco opciones por pregunta y diez segundos para responder. La lectura sigue siendo gratuita; guardar resultados requiere una cuenta de estudiante.'],
  'Select a language, subject and level.': ['Escolha idioma, tema e nível.', 'Elige idioma, tema y nivel.'],
  'These are self-assessments. A course-completion certificate is available only after every chapter test is passed with 10/10 and the entire book passes its editorial completion review. The certificate is not an accredited degree.': ['São autoavaliações. O certificado de conclusão do curso só fica disponível após 10/10 em todos os testes e a aprovação editorial integral do livro. O certificado não é um diploma credenciado.', 'Son autoevaluaciones. El certificado de finalización solo estará disponible tras obtener 10/10 en todas las pruebas y la aprobación editorial completa del libro. El certificado no es un título acreditado.'],
  'Explore': ['Explorar', 'Explorar'],
  'Menu': ['Menu', 'Menú'],
  'Find your course, one choice at a time.': ['Encontre seu curso, uma escolha de cada vez.', 'Encuentra tu curso, una elección a la vez.'],
  'Choose a route, then use the buttons to select your language, subject and level.': ['Escolha uma trilha e use os botões para selecionar idioma, tema e nível.', 'Elige una ruta y usa los botones para seleccionar idioma, tema y nivel.'],
  'How would you like to begin?': ['Como você prefere começar?', '¿Cómo prefieres comenzar?'],
  'Choose a subject or follow every subject in a level.': ['Escolha um tema ou percorra todos os temas de um nível.', 'Elige un tema o recorre todos los temas de un nivel.'],
  'You can change your choice at any step.': ['Você pode alterar sua escolha em qualquer etapa.', 'Puedes cambiar tu elección en cualquier etapa.'],
  'About us': ['Sobre nós', 'Sobre nosotros'],
  'Privacy': ['Privacidade', 'Privacidad'],
  'PRIVACY': ['PRIVACIDADE', 'PRIVACIDAD'],
  'Open study, with optional analytics.': ['Estudo aberto, com análise de uso opcional.', 'Estudio abierto, con análisis de uso opcional.'],
  'Books, lessons, exercises, the public API and MCP can be used without registering or accepting analytics.': ['Livros, aulas, exercícios, a API pública e o MCP podem ser usados sem cadastro e sem aceitar a análise de uso.', 'Los libros, las lecciones, los ejercicios, la API pública y el MCP pueden utilizarse sin registrarse ni aceptar el análisis de uso.'],
  'Optional page-view measurement': ['Medição opcional de visualizações', 'Medición opcional de visitas'],
  'With your permission, the site loads Google Analytics 4 to count page views and understand which public lessons are used. The tag does not load before you choose “Allow analytics”. Page URLs sent from this site omit query parameters. Google may process browser and device information under its own policies.': ['Com sua permissão, o site carrega o Google Analytics 4 para contar visualizações e entender quais aulas públicas são consultadas. A ferramenta não é carregada antes de você escolher “Permitir analytics”. As URLs enviadas por este site não incluem parâmetros de consulta. O Google pode tratar informações do navegador e do dispositivo conforme suas próprias políticas.', 'Con tu permiso, el sitio carga Google Analytics 4 para contar visitas y entender qué lecciones públicas se consultan. La herramienta no se carga antes de elegir “Permitir analytics”. Las URL enviadas por este sitio no incluyen parámetros de consulta. Google puede tratar información del navegador y del dispositivo según sus propias políticas.'],
  "Your choice is kept in this browser's local storage. You can change it using “Analytics preferences” in the footer. A new opt-out stops later page views from this browser, though it does not erase data previously processed by Google.": ['Sua escolha fica armazenada localmente neste navegador. Você pode alterá-la em “Preferências de analytics” no rodapé. Uma nova recusa interrompe visualizações futuras deste navegador, mas não apaga dados já tratados pelo Google.', 'Tu elección se guarda localmente en este navegador. Puedes cambiarla en “Preferencias de analytics” en el pie de página. Rechazar ahora detiene las visitas posteriores desde este navegador, pero no borra datos ya tratados por Google.'],
  'Student progress and chapter tests': ['Progresso do estudante e testes por capítulo', 'Progreso del estudiante y pruebas por capítulo'],
  "You can create and revoke personal MCP keys from your account. D1 stores a key label, prefix, SHA-256 digest, creation and expiration dates, last use and use count, never the complete key. Keys permit your connected AI to read and update your own study records; they expire after 180 days or immediately when revoked. Keep a key in the AI client's private credential storage. Signing out of the browser does not revoke a separately issued key.": ['Você pode criar e revogar chaves MCP pessoais na sua conta. O D1 guarda nome, prefixo, hash SHA-256, datas de criação e expiração, último uso e quantidade de usos, nunca a chave completa. A chave permite que sua IA leia e atualize apenas seus registros de estudo; expira após 180 dias ou imediatamente ao ser revogada. Guarde-a no armazenamento privado de credenciais do cliente de IA. Sair do navegador não revoga uma chave emitida separadamente.', 'Puedes crear y revocar claves MCP personales desde tu cuenta. D1 guarda el nombre, prefijo, hash SHA-256, fechas de creación y caducidad, último uso y número de usos, nunca la clave completa. La clave permite que tu IA lea y actualice solo tus datos de estudio; caduca a los 180 días o al revocarla. Guárdala en el almacenamiento privado de credenciales del cliente de IA. Cerrar la sesión del navegador no revoca una clave emitida por separado.'],
  'Signing in for saved progress and timed tests uses a one-time email code sent by OpenCyber Academy through Cloudflare Email Sending. We do not store a password. Cloudflare D1 stores your email address and student identifier, hashed sign-in codes and session identifiers, lesson and exercise progress, test answers, scores and any course-completion certificate record. Codes expire after 10 minutes; sign-in sessions expire after seven days and can be ended from your account page. Reading books and lessons never requires sign-in.': ['O acesso ao progresso salvo e aos testes cronometrados usa um código único enviado por email pela OpenCyber Academy via Cloudflare Email Sending. Não armazenamos senha. O Cloudflare D1 guarda email e identificador do estudante, códigos e identificadores de sessão em forma de hash, progresso em aulas e exercícios, respostas, notas e eventual certificado. Os códigos expiram em 10 minutos; as sessões expiram em sete dias e podem ser encerradas na página da conta. Ler livros e aulas nunca exige login.', 'El acceso al progreso guardado y a las pruebas cronometradas usa un código único enviado por correo por OpenCyber Academy mediante Cloudflare Email Sending. No guardamos contraseñas. Cloudflare D1 guarda el correo e identificador del estudiante, códigos e identificadores de sesión con hash, progreso en lecciones y ejercicios, respuestas, puntuaciones y posibles certificados. Los códigos caducan en 10 minutos; las sesiones caducan en siete días y pueden cerrarse desde la cuenta. Leer libros y lecciones nunca exige iniciar sesión.'],
  'A public certificate verification link confirms the course, language and issue date without publishing your email address. Test answer keys are public learning material, so these self-assessments are not proctored exams. Reading books and lessons never requires sign-in.': ['O link público de verificação do certificado confirma curso, idioma e data de emissão sem divulgar seu email. Os gabaritos são material público de estudo; portanto, essas autoavaliações não são provas supervisionadas. A leitura dos livros e aulas nunca exige login.', 'El enlace público de verificación del certificado confirma curso, idioma y fecha de emisión sin publicar tu correo. Las respuestas son material de estudio público; por eso estas autoevaluaciones no son exámenes supervisados. Leer libros y lecciones nunca exige iniciar sesión.'],
  'Return to OpenCyber Academy': ['Voltar à OpenCyber Academy', 'Volver a OpenCyber Academy'],
  'About us · OpenCyber Academy': ['Sobre nós · OpenCyber Academy', 'Sobre nosotros · OpenCyber Academy'],
  'ABOUT THE ACADEMY': ['SOBRE A ACADEMIA', 'SOBRE LA ACADEMIA'],
  'Cybersecurity education, open to everyone.': ['Educação em cibersegurança aberta a todos.', 'Educación en ciberseguridad abierta a todos.'],
  'OpenCyber Academy publishes free courses, books, lessons, examples and exercises for people who want to protect others and the technology they depend on. Reading never requires an account.': ['A OpenCyber Academy publica gratuitamente cursos, livros, aulas, exemplos e exercícios para quem deseja proteger pessoas e as tecnologias de que dependem. A leitura não exige uma conta.', 'OpenCyber Academy publica gratuitamente cursos, libros, lecciones, ejemplos y ejercicios para quienes desean proteger a las personas y las tecnologías de las que dependen. Leer nunca requiere una cuenta.'],
  'OUR PURPOSE': ['NOSSO PROPÓSITO', 'NUESTRO PROPÓSITO'],
  'Learn, practice and verify.': ['Aprender, praticar e verificar.', 'Aprender, practicar y verificar.'],
  'Courses are arranged by subject and study level. Each book has its own curriculum, and each authored lesson can be read and cited on this site. A planned study day is labeled as planned until its teaching is published. Editorial review and a complete book are separate milestones.': ['Os cursos são organizados por tema e nível de estudo. Cada livro tem seu currículo, e cada aula escrita pode ser lida e citada neste site. Um dia de estudo planejado continua identificado como planejado até a publicação do conteúdo. Revisão editorial e conclusão de um livro são etapas distintas.', 'Los cursos se organizan por tema y nivel de estudio. Cada libro tiene su propio programa, y cada lección escrita puede leerse y citarse en este sitio. Un día de estudio planificado sigue identificado como tal hasta que se publique su contenido. La revisión editorial y la finalización de un libro son etapas distintas.'],
  'The books and their source Markdown are publicly available. An open API and read-only MCP endpoint let students and other AI systems find the material and check its source.': ['Os livros e seus arquivos Markdown estão disponíveis publicamente. Uma API aberta e um endpoint MCP somente de leitura permitem que estudantes e outros sistemas de IA encontrem o material e verifiquem sua origem.', 'Los libros y sus archivos Markdown están disponibles públicamente. Una API abierta y un endpoint MCP de solo lectura permiten a estudiantes y otros sistemas de IA encontrar el material y verificar su origen.'],
  'Explore the open learning interface →': ['Explore a interface aberta de ensino →', 'Explora la interfaz abierta de aprendizaje →'],
  'FOUNDER': ['FUNDADOR', 'FUNDADOR'],
  'Hiago Kin Levi founded OpenCyber Academy. According to his': ['Hiago Kin Levi fundou a OpenCyber Academy. Segundo sua', 'Hiago Kin Levi fundó OpenCyber Academy. Según su'],
  'professional biography at Decripte': ['biografia profissional na Decripte', 'biografía profesional en Decripte'],
  ', he has worked in information security since 2007 and founded Decripte in 2019 to make enterprise cybersecurity more accessible.': [', ele atua em segurança da informação desde 2007 e fundou a Decripte em 2019 para tornar a cibersegurança empresarial mais acessível.', ', trabaja en seguridad de la información desde 2007 y fundó Decripte en 2019 para hacer más accesible la ciberseguridad empresarial.'],
  'That biography describes his work building and training cybersecurity teams and advising on incident response. It also identifies him as the founder of ABRASECI in 2020 and as president of IBRINC, the Brazilian Institute of Cyber Incident Response.': ['A biografia descreve seu trabalho na implantação e formação de equipes de cibersegurança e na consultoria em resposta a incidentes. Também o identifica como fundador da ABRASECI em 2020 e presidente do IBRINC, Instituto Brasileiro de Resposta a Incidentes Cibernéticos.', 'La biografía describe su trabajo formando equipos de ciberseguridad y asesorando en respuesta a incidentes. También lo identifica como fundador de ABRASECI en 2020 y presidente de IBRINC, el Instituto Brasileño de Respuesta a Incidentes Cibernéticos.'],
  'At OpenCyber Academy, the aim is to make technical learning public, navigable and usable without registration. Course content is identified by language and source so readers can distinguish published teaching from future plans.': ['Na OpenCyber Academy, o objetivo é tornar o ensino técnico público, navegável e acessível sem cadastro. O conteúdo é identificado por idioma e fonte para que o leitor diferencie aulas publicadas de planos futuros.', 'En OpenCyber Academy, el objetivo es hacer que el aprendizaje técnico sea público, navegable y accesible sin registro. El contenido se identifica por idioma y fuente para que el lector distinga las lecciones publicadas de los planes futuros.'],
  "Read the founder's full biography ↗": ['Leia a biografia completa do fundador ↗', 'Lee la biografía completa del fundador ↗'],
  'A preview of the subject learning map': ['Prévia do mapa de estudos', 'Vista previa del mapa de estudios'],
  'Free cybersecurity books, lessons and exercises for everyone who wants to protect people and technology. Choose your path and study without an account.': ['Livros, aulas e exercícios gratuitos de cibersegurança para quem deseja proteger pessoas e tecnologias. Escolha sua trilha e estude sem criar uma conta.', 'Libros, lecciones y ejercicios gratuitos de ciberseguridad para quienes desean proteger a las personas y la tecnología. Elige tu ruta y estudia sin crear una cuenta.'],
  'Begin with the shared concepts; then use them to understand how information must be protected.': ['Comece pelos conceitos em comum; depois use-os para compreender como a informação deve ser protegida.', 'Comienza por los conceptos compartidos; después úsalos para entender cómo debe protegerse la información.'],
  'OPEN CYBER ACADEMY / STUDY ROUTE': ['OPEN CYBER ACADEMY / TRILHA DE ESTUDO', 'OPEN CYBER ACADEMY / RUTA DE ESTUDIO'],
  'BEGIN WITH': ['COMECE POR', 'EMPIEZA POR'],
  'Learn the common language before specializing.': ['Aprenda a linguagem comum antes de se especializar.', 'Aprende el lenguaje común antes de especializarte.'],
  'FOUNDATIONS': ['FUNDAMENTOS', 'FUNDAMENTOS'],
  'DESIGN': ['PROJETO', 'DISEÑO'],
  'OPERATIONS': ['OPERAÇÕES', 'OPERACIONES'],
  'APPLICATION': ['APLICAÇÃO', 'APLICACIÓN'],
  'Understand the landscape': ['Entenda o cenário', 'Comprende el panorama'],
  'Design trustworthy systems': ['Projete sistemas confiáveis', 'Diseña sistemas confiables'],
  'Operate and investigate': ['Opere e investigue', 'Opera e investiga'],
  'Apply in critical settings': ['Aplique em contextos críticos', 'Aplica en entornos críticos'],
  'Explore the 23-area map': ['Explore o mapa das 23 áreas', 'Explora el mapa de 23 áreas'],
  'THE LEARNING MAP': ['MAPA DE ESTUDOS', 'MAPA DE ESTUDIOS'],
  'Twenty-three areas. One connected route.': ['Vinte e três áreas. Uma trilha conectada.', 'Veintitrés áreas. Una ruta conectada.'],
  'Start at 01 and follow the suggested sequence, or open the area you need. Each one adds a different lens to the same security decisions. Choose a study level inside any area.': ['Comece pela 01 e siga a sequência sugerida ou abra a área de que precisa. Cada área acrescenta uma perspectiva às mesmas decisões de segurança. Escolha o nível dentro de qualquer área.', 'Empieza por la 01 y sigue la secuencia sugerida o abre el área que necesites. Cada área aporta una perspectiva a las mismas decisiones de seguridad. Elige el nivel dentro de cualquier área.'],
  'Browse every area ↗': ['Explorar todas as áreas ↗', 'Explorar todas las áreas ↗'],
  'Pause animation': ['Pausar animação', 'Pausar animación'],
  'Play animation': ['Reproduzir animação', 'Reproducir animación'],
  'Finish route': ['Fim da trilha', 'Fin de la ruta'],
  'Study calendar': ['Calendário de estudos', 'Calendario de estudio'],
  'Previous week': ['Semana anterior', 'Semana anterior'],
  'Next week': ['Próxima semana', 'Semana siguiente'],
  'Choose study week': ['Escolha a semana de estudo', 'Elige la semana de estudio'],
  'Study guide': ['Guia de estudo', 'Guía de estudio'],
  'Published lessons in this course': ['Aulas publicadas neste curso', 'Lecciones publicadas en este curso'],
  'Each link opens the complete lesson on its own permanent page. New manuscript edits appear there after publication.': ['Cada link abre o conteúdo completo em uma página permanente. Alterações no livro aparecem após a publicação.', 'Cada enlace abre el contenido completo en una página permanente. Los cambios en el libro aparecen después de publicarse.'],
  'Free cybersecurity education for anyone who wants to protect people and technology. Study published lessons, examples and exercises without creating an account.': ['Educação gratuita em cibersegurança para quem deseja proteger pessoas e tecnologias. Estude aulas, exemplos e exercícios publicados sem criar uma conta.', 'Educación gratuita en ciberseguridad para quienes desean proteger a las personas y la tecnología. Estudia lecciones, ejemplos y ejercicios publicados sin crear una cuenta.'],
  'MONDAY–FRIDAY STUDY PLAN': ['PLANO DE ESTUDO DE SEGUNDA A SEXTA', 'PLAN DE ESTUDIO DE LUNES A VIERNES'],
  'Read the complete book →': ['Ler o livro completo →', 'Leer el libro completo →'],
  'Current public syllabus loaded.': ['Programa público atualizado.', 'Programa público actualizado.'],
  'Loading the current book and lesson guide…': ['Carregando o livro e o guia de aulas…', 'Cargando el libro y la guía de lecciones…'],
  'Choose one study week or browse the complete chapters.': ['Escolha uma semana de estudo ou explore os capítulos completos.', 'Elige una semana de estudio o explora los capítulos completos.'],
  'Daily lessons': ['Aulas diárias', 'Lecciones diarias'],
  'Full chapters': ['Capítulos completos', 'Capítulos completos'],
  'Complete chapters': ['Capítulos completos', 'Capítulos completos'],
  'Read on OpenCyber Academy →': ['Ler no OpenCyber Academy →', 'Leer en OpenCyber Academy →'],
  'Planned · teaching pending': ['Planejada · conteúdo pendente', 'Planificada · contenido pendiente'],
  'View study slot · teaching pending →': ['Ver dia de estudo · conteúdo pendente →', 'Ver día de estudio · contenido pendiente →'],
  'One weekday lesson at a time. Read the explanation and worked example, solve the exercise, then compare the answer. Planned study slots remain clearly marked until teaching is written.': ['Uma aula por dia útil. Leia a explicação e o exemplo comentado, resolva o exercício e compare a resposta. Os dias planejados permanecem identificados até que o conteúdo seja escrito.', 'Una lección por día hábil. Lee la explicación y el ejemplo comentado, resuelve el ejercicio y compara la respuesta. Los días planificados permanecen identificados hasta que se redacte el contenido.'],
  'Study one written lesson at a time. Planned lessons have no teaching text yet.': ['Estude uma aula escrita por vez. Aulas planejadas ainda não têm texto didático.', 'Estudia una lección escrita a la vez. Las lecciones planificadas aún no tienen texto didáctico.'],
  'Read the full subject chapters in this course book.': ['Leia os capítulos completos deste livro.', 'Lee los capítulos completos de este libro.'],
  'This course, week by week': ['Este curso, semana a semana', 'Este curso, semana a semana'],
  'Published course chapters': ['Capítulos publicados do curso', 'Capítulos publicados del curso'],
  'Begin with Day 1 →': ['Comece pelo Dia 1 →', 'Empieza por el Día 1 →'],
  'Begin with Chapter 1 →': ['Comece pelo Capítulo 1 →', 'Empieza por el Capítulo 1 →'],
  'Use the guide at left to choose any week or chapter.': ['Use o guia à esquerda para escolher uma semana ou capítulo.', 'Usa la guía de la izquierda para elegir una semana o capítulo.'],
  'Start with shared language, information, people and the decisions that govern security.': ['Comece pela linguagem comum, informação, pessoas e decisões que orientam a segurança.', 'Empieza por el lenguaje común, la información, las personas y las decisiones que guían la seguridad.'],
  'Turn principles into architecture, identity, networks, platforms and software.': ['Transforme princípios em arquitetura, identidade, redes, plataformas e software.', 'Convierte principios en arquitectura, identidad, redes, plataformas y software.'],
  'Operate, respond and investigate': ['Opere, responda e investigue', 'Opera, responde e investiga'],
  'Detect what changed, contain incidents, examine evidence and test defenses.': ['Detecte mudanças, contenha incidentes, examine evidências e teste defesas.', 'Detecta cambios, contiene incidentes, examina pruebas y evalúa defensas.'],
  'Apply to emerging and critical settings': ['Aplique em contextos emergentes e críticos', 'Aplica en entornos emergentes y críticos'],
  'Carry the same reasoning into AI, post-quantum, industrial and critical systems.': ['Leve o mesmo raciocínio para IA, sistemas pós-quânticos, industriais e críticos.', 'Lleva el mismo razonamiento a IA, sistemas poscuánticos, industriales y críticos.'],
  'Selected area': ['Área selecionada', 'Área seleccionada'],
  'CURRENT STOP': ['ETAPA ATUAL', 'ETAPA ACTUAL'],
  'HOW IT CONNECTS': ['COMO SE CONECTA', 'CÓMO SE CONECTA'],
  'Explore this area ↗': ['Explorar esta área ↗', 'Explorar esta área ↗'],
  'Suggested order · explore freely · 9 levels in each area': ['Ordem sugerida · explore livremente · 9 níveis por área', 'Orden sugerido · explora libremente · 9 niveles por área'],
  'The common vocabulary for threats, controls and systems.': ['O vocabulário comum de ameaças, controles e sistemas.', 'El vocabulario común de amenazas, controles y sistemas.'],
  'Connects cyber controls to information value and handling.': ['Relaciona os controles cibernéticos ao valor e ao tratamento da informação.', 'Relaciona los controles cibernéticos con el valor y el tratamiento de la información.'],
  'Makes ownership, lineage and data decisions explicit.': ['Torna explícitas a titularidade, a linhagem e as decisões sobre dados.', 'Hace explícitas la titularidad, el linaje y las decisiones sobre datos.'],
  'Adds purpose, rights and protection across the data lifecycle.': ['Inclui finalidade, direitos e proteção em todo o ciclo de vida dos dados.', 'Incluye finalidad, derechos y protección en todo el ciclo de vida de los datos.'],
  'Turns technical choices into accountable risk decisions.': ['Transforma escolhas técnicas em decisões de risco com responsáveis.', 'Convierte decisiones técnicas en decisiones de riesgo con responsables.'],
  'Connects policies and human behavior to real operating conditions.': ['Relaciona políticas e comportamento humano às condições reais de operação.', 'Relaciona políticas y comportamiento humano con las condiciones reales de operación.'],
  'Transforms requirements into defensible system boundaries.': ['Transforma requisitos em limites de sistema defensáveis.', 'Convierte requisitos en límites de sistema defendibles.'],
  'Gives systems verifiable confidentiality, integrity and trust.': ['Dá aos sistemas confidencialidade, integridade e confiança verificáveis.', 'Aporta a los sistemas confidencialidad, integridad y confianza verificables.'],
  'Applies assurance to decentralized protocols and assets.': ['Aplica garantias a protocolos e ativos descentralizados.', 'Aplica garantías a protocolos y activos descentralizados.'],
  'Decides who can do what, when and with whose authority.': ['Define quem pode fazer o quê, quando e com qual autoridade.', 'Define quién puede hacer qué, cuándo y con qué autoridad.'],
  'Protects the paths that connect identities and systems.': ['Protege os caminhos que conectam identidades e sistemas.', 'Protege las rutas que conectan identidades y sistemas.'],
  'Secures the hosts, devices and execution layers underneath.': ['Protege hosts, dispositivos e as camadas de execução subjacentes.', 'Protege hosts, dispositivos y las capas de ejecución subyacentes.'],
  'Applies boundaries and ownership to distributed infrastructure.': ['Aplica limites e responsabilidades à infraestrutura distribuída.', 'Aplica límites y responsabilidades a la infraestructura distribuida.'],
  'Builds assurance into software and its dependencies.': ['Incorpora garantias ao software e às suas dependências.', 'Incorpora garantías al software y a sus dependencias.'],
  'Turns telemetry and controls into sustained detection.': ['Transforma telemetria e controles em detecção contínua.', 'Convierte telemetría y controles en detección continua.'],
  'Coordinates decisions, evidence, containment and recovery.': ['Coordena decisões, evidências, contenção e recuperação.', 'Coordina decisiones, pruebas, contención y recuperación.'],
  'Tests incident hypotheses against preserved artifacts.': ['Testa hipóteses do incidente com artefatos preservados.', 'Contrasta hipótesis del incidente con artefactos preservados.'],
  'Adds external context while distinguishing claims from evidence.': ['Acrescenta contexto externo distinguindo alegações de evidências.', 'Añade contexto externo distinguiendo afirmaciones de pruebas.'],
  'Tests assumptions through authorized, bounded adversarial work.': ['Testa premissas por meio de trabalho adversarial autorizado e delimitado.', 'Pone a prueba supuestos mediante trabajo adversarial autorizado y acotado.'],
  'Extends assurance to models, data and AI-enabled workflows.': ['Estende as garantias a modelos, dados e fluxos com IA.', 'Extiende las garantías a modelos, datos y flujos con IA.'],
  'Plans for changing cryptographic assumptions and migration.': ['Planeja a migração diante de mudanças nas premissas criptográficas.', 'Planifica la migración ante cambios en los supuestos criptográficos.'],
  'Adapts security to physical processes, devices and safety.': ['Adapta a segurança a processos físicos, dispositivos e segurança operacional.', 'Adapta la seguridad a procesos físicos, dispositivos y seguridad operativa.'],
  'Integrates the whole path where service failure has broad impact.': ['Integra toda a trilha onde a falha do serviço tem amplo impacto.', 'Integra toda la ruta donde un fallo del servicio tiene gran impacto.'],
  'Shared security vocabulary gives Information security a way to name the information worth protecting.': ['O vocabulário de segurança ajuda Segurança da informação a nomear o que merece proteção.', 'El vocabulario de seguridad ayuda a Seguridad de la información a identificar lo que merece protección.'],
  'Information value leads to Data governance: who owns it, where it moves and how it is used.': ['O valor da informação leva à Governança de dados: quem responde por ela, por onde circula e como é usada.', 'El valor de la información conduce a Gobernanza de datos: quién responde por ella, por dónde circula y cómo se usa.'],
  'Ownership and lineage make Privacy and data protection decisions more precise.': ['Titularidade e linhagem tornam mais precisas as decisões de Privacidade e proteção de dados.', 'Titularidad y linaje hacen más precisas las decisiones de Privacidad y protección de datos.'],
  'Data rights and purpose become accountable choices in Security governance, risk and compliance.': ['Direitos e finalidade dos dados tornam-se escolhas com responsáveis em Governança, risco e conformidade.', 'Los derechos y la finalidad de los datos se convierten en decisiones responsables de Gobierno, riesgo y cumplimiento.'],
  'Governance needs people who can carry it out; Human factors and policy examines that reality.': ['A governança depende de pessoas para executá-la; Fatores humanos e política examina essa realidade.', 'El gobierno depende de personas para llevarlo a cabo; Factores humanos y política examina esa realidad.'],
  'People and rules set requirements that Security architecture must make operational.': ['Pessoas e regras estabelecem requisitos que a Arquitetura de segurança precisa tornar operacionais.', 'Personas y reglas establecen requisitos que la Arquitectura de seguridad debe llevar a la práctica.'],
  'Architecture needs verifiable trust mechanisms; Cryptography supplies some of them.': ['A arquitetura precisa de mecanismos verificáveis de confiança; a Criptografia fornece parte deles.', 'La arquitectura necesita mecanismos verificables de confianza; la Criptografía aporta algunos.'],
  'Trust assumptions are stress-tested in decentralized systems and cryptoassets.': ['Premissas de confiança são testadas em sistemas descentralizados e criptoativos.', 'Los supuestos de confianza se ponen a prueba en sistemas descentralizados y criptoactivos.'],
  'Identity and access connects trust mechanisms to people, services and authority.': ['Identidade e acesso conectam mecanismos de confiança a pessoas, serviços e autoridade.', 'Identidad y acceso conectan mecanismos de confianza con personas, servicios y autoridad.'],
  'Authorized identities use communication paths; Network security protects those paths.': ['Identidades autorizadas usam canais de comunicação; Segurança de redes protege esses caminhos.', 'Las identidades autorizadas usan canales de comunicación; Seguridad de redes protege esas rutas.'],
  'Network controls depend on the endpoints and hardware at either end.': ['Controles de rede dependem dos dispositivos e do hardware em cada ponta.', 'Los controles de red dependen de los dispositivos y del hardware en cada extremo.'],
  'Host boundaries extend into Cloud and container operations.': ['Os limites dos hosts se estendem às operações em Nuvem e contêineres.', 'Los límites de los hosts se extienden a las operaciones en Nube y contenedores.'],
  'Cloud workloads are built and updated through the Application supply chain.': ['Cargas de trabalho em nuvem são criadas e atualizadas pela Cadeia de software.', 'Las cargas de trabajo en nube se crean y actualizan mediante la Cadena de software.'],
  'Deployed systems produce the signals that Security operations must interpret.': ['Sistemas implantados produzem sinais que Operações de segurança precisam interpretar.', 'Los sistemas desplegados producen señales que Operaciones de seguridad debe interpretar.'],
  'Detection becomes useful when Incident response can make bounded, evidenced decisions.': ['A detecção ganha utilidade quando a Resposta a incidentes toma decisões delimitadas e fundamentadas.', 'La detección resulta útil cuando Respuesta a incidentes toma decisiones acotadas y fundamentadas.'],
  'Incident hypotheses need preserved evidence; Digital forensics tests them.': ['Hipóteses do incidente precisam de evidências preservadas; Perícia digital as testa.', 'Las hipótesis del incidente requieren pruebas conservadas; Análisis forense digital las evalúa.'],
  'Forensic observations gain context from Threat intelligence and OSINT.': ['Observações forenses ganham contexto com Inteligência de ameaças e OSINT.', 'Las observaciones forenses ganan contexto con Inteligencia de amenazas y OSINT.'],
  'External context becomes testable assumptions in authorized Offensive security exercises.': ['O contexto externo vira premissas testáveis em exercícios autorizados de Segurança ofensiva.', 'El contexto externo se convierte en supuestos comprobables en ejercicios autorizados de Seguridad ofensiva.'],
  'The same bounded testing mindset helps examine AI systems and their workflows.': ['A mesma abordagem de testes delimitados ajuda a examinar sistemas e fluxos de IA.', 'El mismo enfoque de pruebas acotadas ayuda a examinar sistemas y flujos de IA.'],
  'AI systems still depend on cryptography; Quantum and post-quantum planning revisits its assumptions.': ['Sistemas de IA ainda dependem de criptografia; o planejamento quântico e pós-quântico revisita suas premissas.', 'Los sistemas de IA aún dependen de la criptografía; la planificación cuántica y poscuántica revisa sus supuestos.'],
  'Migration planning must account for long-lived OT, IoT and physical systems.': ['O planejamento de migração precisa considerar sistemas OT, IoT e físicos de longa vida.', 'La planificación de la migración debe considerar sistemas OT, IoT y físicos de larga duración.'],
  'Physical-process constraints converge in Critical infrastructure and sector security.': ['As restrições dos processos físicos convergem em Infraestrutura crítica e segurança setorial.', 'Las limitaciones de los procesos físicos convergen en Infraestructura crítica y seguridad sectorial.'],
  'End of the suggested area route. Revisit any subject at a deeper level or follow its course lessons.': ['Fim da sequência sugerida. Retorne a qualquer tema em um nível mais profundo ou siga as aulas do curso.', 'Final de la secuencia sugerida. Vuelve a cualquier tema en un nivel más profundo o sigue las lecciones del curso.'],
  'Skip to content': ['Pular para o conteúdo', 'Saltar al contenido'],
  'OpenCyber Academy, home': ['OpenCyber Academy, início', 'OpenCyber Academy, inicio'],
  'Main navigation': ['Navegação principal', 'Navegación principal'],
  'Start here': ['Comece por aqui', 'Empieza aquí'],
  'Courses': ['Cursos', 'Cursos'],
  'Browse courses': ['Explorar cursos', 'Explorar cursos'],
  'By level': ['Por nível', 'Por nivel'],
  'By subject': ['Por tema', 'Por tema'],
  'All levels →': ['Todos os níveis →', 'Todos los niveles →'],
  'All subjects →': ['Todos os temas →', 'Todos los temas →'],
  'Choose a level, then a course': ['Escolha um nível e depois um curso', 'Elige un nivel y luego un curso'],
  'Choose a subject, then a level': ['Escolha um tema e depois um nível', 'Elige un tema y luego un nivel'],
  'Loading courses…': ['Carregando cursos…', 'Cargando cursos…'],
  'View this group →': ['Ver este grupo →', 'Ver este grupo →'],
  'Rapid course': ['Curso rápido', 'Curso rápido'],
  'Professional': ['Profissionalizante', 'Profesional'],
  'Technical': ['Técnico', 'Técnico'],
  'Technologist': ['Tecnólogo', 'Tecnólogo'],
  "Bachelor's": ['Graduação', 'Grado'],
  'Engineering': ['Engenharia', 'Ingeniería'],
  'Postgraduate': ['Pós-graduação', 'Posgrado'],
  "Master's": ['Mestrado', 'Máster'],
  'Doctoral research': ['Pesquisa doutoral', 'Investigación doctoral'],
  'COURSE DIRECTORY': ['DIRETÓRIO DE CURSOS', 'DIRECTORIO DE CURSOS'],
  'Browse by level.': ['Explore por nível.', 'Explora por nivel.'],
  'Browse by subject.': ['Explore por tema.', 'Explora por tema.'],
  'Choose a level, then open one of its 23 separate courses. Every course has its own lesson guide and book.': ['Escolha um nível e abra um dos 23 cursos separados. Cada curso tem seu guia de aulas e livro.', 'Elige un nivel y abre uno de sus 23 cursos independientes. Cada curso tiene su guía de lecciones y libro.'],
  'Choose a subject, then a level. Each combination opens its own course and lessons.': ['Escolha um tema e depois um nível. Cada combinação abre seu próprio curso e aulas.', 'Elige un tema y luego un nivel. Cada combinación abre su propio curso y lecciones.'],
  '23 separate courses · Choose a subject and open its lessons.': ['23 cursos separados · Escolha um tema e abra as aulas.', '23 cursos separados · Elige un tema y abre las lecciones.'],
  '9 separate study levels · Choose the course that fits you.': ['9 níveis separados · Escolha o curso para você.', '9 niveles separados · Elige el curso adecuado.'],
  'Explore courses →': ['Explorar cursos →', 'Explorar cursos →'],
  'Choose a level →': ['Escolher nível →', 'Elegir nivel →'],
  'Levels': ['Níveis', 'Niveles'],
  'Subjects': ['Temas', 'Temas'],
  'All levels': ['Todos os níveis', 'Todos los niveles'],
  'All subjects': ['Todos os temas', 'Todos los temas'],
  'Browse by level': ['Explorar por nível', 'Explorar por nivel'],
  'Browse by subject': ['Explorar por tema', 'Explorar por tema'],
  'Each subject below is a separate course with its own book and lesson navigation. Follow the curriculum order or choose the subject you need.': ['Cada tema abaixo é um curso separado, com livro e navegação de aulas próprios. Siga a ordem curricular ou escolha o tema desejado.', 'Cada tema es un curso independiente, con libro y navegación de lecciones propios. Sigue el orden curricular o elige el tema que necesites.'],
  'Choose your level. Each course has its own chapter list, book and lesson navigation.': ['Escolha seu nível. Cada curso tem sua lista de capítulos, livro e navegação de aulas.', 'Elige tu nivel. Cada curso tiene su lista de capítulos, libro y navegación de lecciones.'],
  'Open course →': ['Abrir curso →', 'Abrir curso →'],
  'Start first lesson →': ['Começar pela primeira aula →', 'Empezar por la primera lección →'],
  'Previous level': ['Nível anterior', 'Nivel anterior'],
  'Next level →': ['Próximo nível →', 'Siguiente nivel →'],
  '← Previous course': ['← Curso anterior', '← Curso anterior'],
  'All courses at this level': ['Todos os cursos deste nível', 'Todos los cursos de este nivel'],
  'All courses at this level →': ['Todos os cursos deste nível →', 'Todos los cursos de este nivel →'],
  'Other levels in this subject →': ['Outros níveis deste tema →', 'Otros niveles de este tema →'],
  'Course language': ['Idioma do curso', 'Idioma del curso'],
  'COURSE CONTENTS': ['CONTEÚDO DO CURSO', 'CONTENIDO DEL CURSO'],
  'Modules and lessons': ['Módulos e aulas', 'Módulos y lecciones'],
  'Chapters and lessons': ['Capítulos e aulas', 'Capítulos y lecciones'],
  'Open each chapter to find its daily lessons.': ['Abra cada capítulo para encontrar as aulas diárias.', 'Abre cada capítulo para encontrar las lecciones diarias.'],
  'Published chapters and current curriculum blocks.': ['Capítulos publicados e blocos curriculares atuais.', 'Capítulos publicados y bloques curriculares actuales.'],
  'WEEKDAY STUDY PLAN': ['PLANO DE ESTUDO EM DIAS ÚTEIS', 'PLAN DE ESTUDIO DE LUNES A VIERNES'],
  'HOW TO STUDY': ['COMO ESTUDAR', 'CÓMO ESTUDIAR'],
  'One idea, taught properly': ['Uma ideia, ensinada com rigor', 'Una idea, enseñada con rigor'],
  'Minimum lessons, no maximum': ['Mínimo de aulas, sem máximo', 'Mínimo de lecciones, sin máximo'],
  'Study one lesson on a weekday. The planning minimum for this level is a floor. If an idea needs another lesson to be taught well, the course grows. Chapter length follows the idea.': ['Estude uma aula por dia útil. O mínimo deste nível é um piso. Se uma ideia precisar de outra aula para ser bem ensinada, o curso cresce. O tamanho do capítulo segue a ideia.', 'Estudia una lección por día hábil. El mínimo de este nivel es un piso. Si una idea necesita otra lección para enseñarse bien, el curso crece. El tamaño del capítulo sigue la idea.'],
  'English lessons first': ['Aulas em inglês primeiro', 'Lecciones en inglés primero'],
  'A lesson is as long as the idea needs. Read the explanation, follow the worked example, then try the exercise. There is no required chapter length or lesson quota.': ['A aula tem o tamanho que a ideia pede. Leia a explicação, acompanhe o exemplo resolvido e faça o exercício. Não há tamanho obrigatório nem cota de aulas.', 'La lección tiene el tamaño que la idea pide. Lee la explicación, sigue el ejemplo resuelto y haz el ejercicio. No hay tamaño obligatorio ni cuota de lecciones.'],
  'Length follows the idea': ['O tamanho segue a ideia', 'El tamaño sigue la idea'],
  'English first, then translation': ['Inglês primeiro, depois a tradução', 'Inglés primero, luego la traducción'],
  'One chapter each Monday–Friday: learn the concept, follow a worked example, then solve an exercise. The plan applies to every language edition.': ['Um capítulo de segunda a sexta: aprenda o conceito, acompanhe um exemplo resolvido e faça um exercício. O plano vale para todos os idiomas.', 'Un capítulo de lunes a viernes: aprende el concepto, sigue un ejemplo resuelto y haz un ejercicio. El plan se aplica a todos los idiomas.'],
  'One lesson each Monday–Friday, normally five lessons in a weekly chapter. Learn the concept, follow a worked example, then solve an exercise. The plan applies to every language edition.': ['Uma aula por dia útil, normalmente cinco aulas em cada capítulo semanal. Aprenda o conceito, acompanhe um exemplo resolvido e faça um exercício. O plano vale para todos os idiomas.', 'Una lección por día hábil, normalmente cinco lecciones en cada capítulo semanal. Aprende el concepto, sigue un ejemplo resuelto y resuelve un ejercicio. El plan se aplica a todos los idiomas.'],
  'Mon': ['Seg', 'Lun'], 'Tue': ['Ter', 'Mar'], 'Wed': ['Qua', 'Mié'], 'Thu': ['Qui', 'Jue'], 'Fri': ['Sex', 'Vie'],
  'One course, one book. The study target is one chapter each weekday, with a worked example and an exercise. Read the chapters already published below.': ['Um curso, um livro. A meta é um capítulo por dia útil, com exemplo resolvido e exercício. Leia abaixo os capítulos já publicados.', 'Un curso, un libro. La meta es un capítulo por día hábil, con ejemplo resuelto y ejercicio. Lee abajo los capítulos ya publicados.'],
  'One course, one book. Study one lesson each weekday, normally in a weekly chapter with five lessons. Each lesson has a worked example and an exercise. Read what is published below.': ['Um curso, um livro. Estude uma aula por dia útil, normalmente em um capítulo semanal de cinco aulas. Cada aula traz um exemplo resolvido e um exercício. Leia abaixo o que já foi publicado.', 'Un curso, un libro. Estudia una lección por día hábil, normalmente en un capítulo semanal de cinco lecciones. Cada lección incluye un ejemplo resuelto y un ejercicio. Lee lo ya publicado.'],
  'Follow the subjects in their curricular order.': ['Siga as matérias na ordem curricular.', 'Sigue las materias en orden curricular.'],
  '← Course overview': ['← Visão geral do curso', '← Vista general del curso'],
  'Course overview': ['Visão geral do curso', 'Vista general del curso'],
  'Your course roadmap': ['Seu roteiro do curso', 'Tu recorrido del curso'],
  'Read lesson →': ['Ler aula →', 'Leer lección →'],
  'Not published': ['Ainda não publicada', 'Aún no publicada'],
  'This lesson has not been published in this edition yet. Choose another available lesson or return to the course overview.': ['Esta aula ainda não foi publicada nesta edição. Escolha outra aula disponível ou volte à visão geral do curso.', 'Esta lección aún no se ha publicado en esta edición. Elige otra disponible o vuelve a la vista general del curso.'],
  'Jump to exercises ↓': ['Ir para os exercícios ↓', 'Ir a los ejercicios ↓'],
  'One course, one book. Read its lessons in order, or open the full book. Each lesson keeps its exercises and worked answers together.': ['Um curso, um livro. Leia as aulas em ordem ou abra o livro completo. Cada aula reúne exercícios e respostas comentadas.', 'Un curso, un libro. Lee las lecciones en orden o abre el libro completo. Cada lección reúne ejercicios y respuestas desarrolladas.'],
  'Choose a chapter to read on this page.': ['Escolha um capítulo para ler nesta página.', 'Elige un capítulo para leer en esta página.'],
  'Loading this course…': ['Carregando este curso…', 'Cargando este curso…'],
  'Course guide loaded.': ['Guia do curso carregado.', 'Guía del curso cargada.'],
  'Start first published lesson →': ['Começar pela primeira aula publicada →', 'Comenzar por la primera lección publicada →'],
  'Choose a course.': ['Escolha um curso.', 'Elige un curso.'],
  'Use the level menu to see all subjects at one study level, or the subject menu to compare that subject across levels. Each course opens on its own page.': ['Use o menu por nível para ver todos os temas de um nível, ou o menu por tema para comparar os níveis desse tema. Cada curso abre em sua própria página.', 'Usa el menú por nivel para ver todos los temas de un nivel, o el menú por tema para comparar sus niveles. Cada curso se abre en su propia página.'],
  '← Previous level': ['← Nível anterior', '← Nivel anterior'],
  '23 separate courses': ['23 cursos separados', '23 cursos separados'],
  '9 separate courses': ['9 cursos separados', '9 cursos separados'],
  'Browse all courses': ['Explore todos os cursos', 'Explora todos los cursos'],
  'Choose a course using the menus above.': ['Escolha um curso nos menus acima.', 'Elige un curso en los menús de arriba.'],
  'For AIs': ['Para IAs', 'Para IA'],
  'Editorial standard': ['Padrão editorial', 'Estándar editorial'],
  'Site language': ['Idioma do site', 'Idioma del sitio'],
  'Toggle light and dark theme': ['Alternar tema claro e escuro', 'Cambiar entre tema claro y oscuro'],
  'Toggle theme': ['Alternar tema', 'Cambiar tema'],
  'My area': ['Minha área', 'Mi área'],
  'Connect your AI': ['Conecte sua IA', 'Conecta tu IA'],
  'Connect your AI →': ['Conecte sua IA →', 'Conecta tu IA →'],
  'PRIVATE STUDENT MCP': ['MCP PRIVADO DO ESTUDANTE', 'MCP PRIVADO DEL ESTUDIANTE'],
  'Connect your AI to your own study record.': ['Conecte sua IA ao seu próprio histórico de estudos.', 'Conecta tu IA a tu propio historial de estudios.'],
  'Sign in to your student area and create a personal key in “Connect your AI”. Use an MCP client that supports private HTTP headers:': ['Entre na sua área de estudante e crie uma chave pessoal em “Conecte sua IA”. Use um cliente MCP que aceite cabeçalhos HTTP privados:', 'Entra en tu área de estudiante y crea una clave personal en “Conecta tu IA”. Usa un cliente MCP que admita encabezados HTTP privados:'],
  "The key appears once. Keep it in the client's private credential field, never in a prompt or a URL. It expires after 180 days and can be revoked from your account. Authenticated study actions count toward your own dashboard.": ['A chave aparece uma única vez. Guarde-a no campo privado de credenciais do cliente, nunca em um prompt ou URL. Ela expira em 180 dias e pode ser revogada na sua conta. As ações de estudo autenticadas entram no seu painel.', 'La clave aparece una sola vez. Guárdala en el campo privado de credenciales del cliente, nunca en un prompt ni en una URL. Caduca a los 180 días y puedes revocarla desde tu cuenta. Las acciones de estudio autenticadas se reflejan en tu panel.'],
  'Student tools can record lesson visits, completion, exercise answers, analyses and timed chapter tests, then read progress and results. Public books remain readable without signing in.': ['As ferramentas de estudante podem registrar visitas às aulas, conclusão, respostas de exercícios, análises e testes cronometrados, além de consultar progresso e resultados. Os livros públicos continuam acessíveis sem login.', 'Las herramientas de estudiante pueden registrar visitas a lecciones, finalización, respuestas de ejercicios, análisis y pruebas cronometradas, además de consultar progreso y resultados. Los libros públicos siguen disponibles sin iniciar sesión.'],
  'Open learning library': ['Biblioteca de estudo aberta', 'Biblioteca de estudio abierta'],
  'Rights': ['Direitos', 'Derechos'],
  'Books and courses': ['Livros e cursos', 'Libros y cursos'],
  'OPEN LIBRARY · PUBLIC SOURCE': ['BIBLIOTECA ABERTA · FONTE PÚBLICA', 'BIBLIOTECA ABIERTA · FUENTE PÚBLICA'],
  'Learn to think about': ['Aprenda a pensar em', 'Aprende a pensar en'],
  'Learn cybersecurity through': ['Aprenda cibersegurança com', 'Aprende ciberseguridad con'],
  'open lessons and practice.': ['aulas abertas e prática.', 'lecciones abiertas y práctica.'],
  'Choose a subject and study level. Read published teaching, work through an example, try an exercise and compare the explained answer. Free to read, with no account required.': ['Escolha um tema e nível de estudo. Leia as aulas publicadas, acompanhe um exemplo, tente um exercício e compare a resposta explicada. A leitura é gratuita e não exige conta.', 'Elige un tema y un nivel de estudio. Lee las lecciones publicadas, sigue un ejemplo, intenta un ejercicio y compara la respuesta explicada. Puedes leer gratis y sin cuenta.'],
  'security': ['segurança', 'seguridad'],
  'clearly.': ['com clareza.', 'con claridad.'],
  'A journey through cybersecurity books, lessons and exercises for people and AI systems. Choose your path and study without an account.': ['Uma jornada por livros, aulas e exercícios de cibersegurança para pessoas e sistemas de IA. Escolha seu caminho e estude sem cadastro.', 'Un recorrido por libros, lecciones y ejercicios de ciberseguridad para personas y sistemas de IA. Elige tu camino y estudia sin registrarte.'],
  'Choose your path': ['Escolha sua trilha', 'Elige tu ruta'],
  'Read a sample lesson (English)': ['Ler uma aula de exemplo (em inglês)', 'Leer una lección de ejemplo (en inglés)'],
  'Connect an AI': ['Conectar uma IA', 'Conectar una IA'],
  'Open lessons': ['Aulas abertas', 'Lecciones abiertas'],
  'Read without signing in': ['Leia sem criar conta', 'Lee sin registrarte'],
  'Worked practice': ['Prática com resolução', 'Práctica resuelta'],
  'Examples, exercises and answers': ['Exemplos, exercícios e respostas', 'Ejemplos, ejercicios y respuestas'],
  'Clear next steps': ['Próximos passos claros', 'Próximos pasos claros'],
  'Follow published teaching': ['Siga as aulas publicadas', 'Sigue las lecciones publicadas'],
  'Abstract illustration of learning paths': ['Ilustração das trilhas de aprendizagem', 'Ilustración de las rutas de aprendizaje'],
  'Knowledge': ['Conhecimento', 'Conocimiento'],
  'technical, open': ['técnico, aberto', 'técnico, abierto'],
  'One lesson per chapter': ['Uma aula por capítulo', 'Una lección por capítulo'],
  'One lesson each weekday': ['Uma aula por dia útil', 'Una lección por día hábil'],
  'five in a weekly chapter': ['cinco em um capítulo semanal', 'cinco en un capítulo semanal'],
  'with exercises': ['com exercícios', 'con ejercicios'],
  'Living source': ['Fonte viva', 'Fuente viva'],
  'books kept current': ['livros atualizados', 'libros actualizados'],
  'START HERE': ['COMECE POR AQUI', 'EMPIEZA AQUÍ'],
  'Two ways to find your next lesson.': ['Duas formas de chegar à próxima aula.', 'Dos maneras de encontrar tu próxima lección.'],
  'Choose your route. Both paths show every subject in order and open chapters that have teaching text.': ['Escolha sua trilha. Ambas mostram todas as matérias em ordem e abrem os capítulos com texto didático.', 'Elige tu ruta. Ambas muestran todas las materias en orden y abren los capítulos con contenido didáctico.'],
  'I have a subject in mind': ['Tenho um tema em mente', 'Tengo un tema en mente'],
  'Choose a language, subject and level. Open the course and follow its lessons in order.': ['Escolha idioma, tema e nível. Abra o curso e siga as aulas em ordem.', 'Elige idioma, tema y nivel. Abre el curso y sigue las lecciones en orden.'],
  'Language': ['Idioma', 'Idioma'],
  'Subject': ['Tema', 'Tema'],
  'Level': ['Nível', 'Nivel'],
  '1. Language': ['1. Idioma', '1. Idioma'],
  '2. Subject': ['2. Tema', '2. Tema'],
  '3. Level': ['3. Nível', '3. Nivel'],
  '2. Level': ['2. Nível', '2. Nivel'],
  'Open course': ['Abrir curso', 'Abrir curso'],
  'I want to study a whole level': ['Quero estudar um nível inteiro', 'Quiero estudiar un nivel completo'],
  'Choose a language and level. Browse all 23 subjects in curriculum order, with their lesson guides.': ['Escolha idioma e nível. Veja os 23 temas em ordem curricular, com seus guias de aula.', 'Elige idioma y nivel. Consulta los 23 temas en orden curricular, con sus guías de lecciones.'],
  '23 subjects': ['23 temas', '23 temas'],
  'Move from the first subject to the last, lesson by lesson, with each book in reach.': ['Avance do primeiro ao último tema, aula por aula, com cada livro ao alcance.', 'Avanza del primer al último tema, lección por lección, con cada libro a mano.'],
  'View all subjects': ['Ver todos os temas', 'Ver todos los temas'],
  'Loading the public catalog…': ['Carregando o catálogo público…', 'Cargando el catálogo público…'],
  'Catalog loaded. Each lesson is read from the current public manuscript.': ['Catálogo carregado. Cada aula vem do manuscrito público atual.', 'Catálogo cargado. Cada lección proviene del manuscrito público actual.'],
  'FROM CONCEPT TO PRACTICE': ['DO CONCEITO À PRÁTICA', 'DEL CONCEPTO A LA PRÁCTICA'],
  'Learning you can verify.': ['Aprendizado que você pode verificar.', 'Aprendizaje que puedes verificar.'],
  'Each course has one book. Subjects organize modules, and the study target is one chapter every weekday, with a worked example and an exercise. The reader shows what is published and keeps previous, index and next navigation close to each lesson.': ['Cada curso tem um livro. As matérias organizam módulos; a meta é um capítulo por dia útil, com exemplo resolvido e exercício. O leitor mostra o que foi publicado e mantém a navegação entre aulas.', 'Cada curso tiene un libro. Las materias organizan módulos; la meta es un capítulo por día hábil, con ejemplo resuelto y ejercicio. El lector muestra lo publicado y mantiene la navegación entre lecciones.'],
  'Each course has one book. Subjects organize modules, weekly chapters group daily lessons, and each lesson has a worked example and an exercise. The reader shows what is published and keeps previous, index and next navigation close to each lesson.': ['Cada curso tem um livro. As matérias organizam módulos, os capítulos semanais reúnem aulas diárias e cada aula tem exemplo resolvido e exercício. O leitor mostra o que foi publicado e mantém a navegação entre aulas.', 'Cada curso tiene un libro. Las materias organizan módulos, los capítulos semanales reúnen lecciones diarias y cada lección tiene un ejemplo resuelto y un ejercicio. El lector muestra lo publicado y mantiene la navegación entre lecciones.'],
  'Read the editorial standard →': ['Leia o padrão editorial →', 'Lee el estándar editorial →'],
  'Transparent source': ['Fonte transparente', 'Fuente transparente'],
  'Open text with its course and edition identified.': ['Texto aberto com curso e edição identificados.', 'Texto abierto con curso y edición identificados.'],
  'No entry barrier': ['Sem barreira de entrada', 'Sin barreras de acceso'],
  'Read courses, books and exercises without an account.': ['Leia cursos, livros e exercícios sem cadastro.', 'Lee cursos, libros y ejercicios sin registrarte.'],
  'Ready for other AIs': ['Pronto para outras IAs', 'Listo para otras IA'],
  'Public API, Markdown and read-only MCP server.': ['API pública, Markdown e servidor MCP de leitura.', 'API pública, Markdown y servidor MCP de solo lectura.'],
  'FOR SYSTEMS AND AGENTS': ['PARA SISTEMAS E AGENTES', 'PARA SISTEMAS Y AGENTES'],
  'A library other AIs can consult.': ['Uma biblioteca que outras IAs podem consultar.', 'Una biblioteca que otras IA pueden consultar.'],
  'ChatGPT, Claude, DAI and other tools can discover courses and read lessons through MCP or the open API. Every response identifies its public manuscript.': ['ChatGPT, Claude, DAI e outras ferramentas podem descobrir cursos e ler aulas por MCP ou pela API aberta. Cada resposta identifica seu manuscrito público.', 'ChatGPT, Claude, DAI y otras herramientas pueden descubrir cursos y leer lecciones por MCP o la API abierta. Cada respuesta identifica su manuscrito público.'],
  'Explore MCP access →': ['Explorar acesso MCP →', 'Explorar acceso MCP →'],
  'STUDY ROOM · OPEN ACCESS': ['SALA DE ESTUDO · ACESSO ABERTO', 'SALA DE ESTUDIO · ACCESO ABIERTO'],
  'Your path through knowledge.': ['Seu caminho pelo conhecimento.', 'Tu camino por el conocimiento.'],
  'Choose a route and move through the published lessons. Planned chapters are identified and never presented as finished lessons.': ['Escolha uma trilha e avance pelas aulas publicadas. Capítulos planejados são identificados e nunca apresentados como aulas prontas.', 'Elige una ruta y avanza por las lecciones publicadas. Los capítulos planificados se identifican y nunca se presentan como lecciones terminadas.'],
  'Route': ['Trilha', 'Ruta'],
  'Subject → level': ['Tema → nível', 'Tema → nivel'],
  'Level → all subjects': ['Nível → todos os temas', 'Nivel → todos los temas'],
  'Course and lesson guide': ['Guia de cursos e aulas', 'Guía de cursos y lecciones'],
  'COURSE GUIDE': ['GUIA DO CURSO', 'GUÍA DEL CURSO'],
  'Choose a route.': ['Escolha uma trilha.', 'Elige una ruta.'],
  'Choose a course to begin.': ['Escolha um curso para começar.', 'Elige un curso para empezar.'],
  'The guide shows subjects in order and marks chapters with published lesson text.': ['O guia mostra as matérias em ordem e marca os capítulos com aulas publicadas.', 'La guía muestra las materias en orden y marca los capítulos con lecciones publicadas.'],
  'View worked answers': ['Ver respostas comentadas', 'Ver respuestas desarrolladas'],
  'YOUR PROGRESS · OPTIONAL': ['SEU PROGRESSO · OPCIONAL', 'TU PROGRESO · OPCIONAL'],
  'Save this lesson': ['Salvar esta aula', 'Guardar esta lección'],
  'Reading is open without an account. Saving progress with optional sign-in will be added later.': ['A leitura está aberta sem conta. O salvamento do progresso com login opcional será adicionado depois.', 'La lectura está abierta sin cuenta. El guardado del progreso con inicio de sesión opcional se añadirá después.'],
  'Lessons in this course': ['Aulas neste curso', 'Lecciones de este curso'],
  '23 subjects in study order': ['23 temas na ordem de estudo', '23 temas en orden de estudio'],
  'Choose a level for this subject': ['Escolha um nível para este tema', 'Elige un nivel para este tema'],
  'Open published lesson': ['Abrir aula publicada', 'Abrir lección publicada'],
  'Planned chapter': ['Capítulo planejado', 'Capítulo planificado'],
  'Loading the course guide…': ['Carregando o guia do curso…', 'Cargando la guía del curso…'],
  'Loading the current course plan and book…': ['Carregando plano e livro atuais…', 'Cargando el plan y libro actuales…'],
  'Read the full book here →': ['Leia o livro completo aqui →', 'Lee el libro completo aquí →'],
  'Read the course plan here →': ['Leia o plano do curso aqui →', 'Lee el plan del curso aquí →'],
  'This course could not be loaded.': ['Não foi possível carregar este curso.', 'No se pudo cargar este curso.'],
  'This course is temporarily unavailable. Please try again shortly.': ['Curso temporariamente indisponível. Tente novamente em breve.', 'Curso temporalmente no disponible. Inténtalo de nuevo pronto.'],
  'Sign-in unavailable': ['Login indisponível', 'Inicio de sesión no disponible'],
  'Sign in to save progress →': ['Entre para salvar progresso →', 'Inicia sesión para guardar el progreso →'],
  'Progress saving is coming later. Continue reading without an account.': ['O salvamento do progresso virá depois. Continue lendo sem conta.', 'El guardado del progreso llegará después. Sigue leyendo sin cuenta.'],
  'Mark lesson complete ✓': ['Marcar aula como concluída ✓', 'Marcar lección como completada ✓'],
  'Lesson completed and saved to your account.': ['Aula concluída e salva na sua conta.', 'Lección completada y guardada en tu cuenta.'],
  'Could not save right now.': ['Não foi possível salvar agora.', 'No se pudo guardar ahora.'],
  'Save your attempt, then compare the worked answer.': ['Salve sua tentativa e compare com a resposta comentada.', 'Guarda tu intento y compáralo con la respuesta desarrollada.'],
  'Save attempt': ['Salvar tentativa', 'Guardar intento'],
  'Read this chapter in the book →': ['Leia este capítulo no livro →', 'Lee este capítulo en el libro →'],
  'Read the chapter plan →': ['Leia o plano do capítulo →', 'Lee el plan del capítulo →'],
  'This subject is in the course plan. Its lesson text has not been published in this edition.': ['Esta matéria está no plano do curso. A aula ainda não foi publicada nesta edição.', 'Esta materia está en el plan del curso. La lección aún no se ha publicado en esta edición.'],
  'Loading the published lesson…': ['Carregando a aula publicada…', 'Cargando la lección publicada…'],
  'The lesson is temporarily unavailable.': ['Aula temporariamente indisponível.', 'Lección temporalmente no disponible.'],
  '← Previous lesson': ['← Aula anterior', '← Lección anterior'],
  'Course guide': ['Guia do curso', 'Guía del curso'],
  'Next lesson →': ['Próxima aula →', 'Siguiente lección →'],
  'Next course →': ['Próximo curso →', 'Siguiente curso →'],
  'Choose a course to read its public book.': ['Escolha um curso para ler seu livro público.', 'Elige un curso para leer su libro público.'],
  'The catalog is temporarily unavailable.': ['O catálogo está temporariamente indisponível.', 'El catálogo no está disponible temporalmente.'],
  'OPEN BOOK · NO ACCOUNT REQUIRED': ['LIVRO ABERTO · SEM CADASTRO', 'LIBRO ABIERTO · SIN REGISTRO'],
  'Public course book': ['Livro público do curso', 'Libro público del curso'],
  'Loading the current book…': ['Carregando o livro atual…', 'Cargando el libro actual…'],
  'Course lesson guide →': ['Guia de aulas do curso →', 'Guía de lecciones del curso →'],
  'CHAPTERS': ['CAPÍTULOS', 'CAPÍTULOS'],
  'CHAPTERS & LESSONS': ['CAPÍTULOS E AULAS', 'CAPÍTULOS Y LECCIONES'],
  'Book chapters and lessons': ['Capítulos e aulas do livro', 'Capítulos y lecciones del libro'],
  'Book chapters': ['Capítulos do livro', 'Capítulos del libro'],
  'Choose a course from the study guide.': ['Escolha um curso no guia de estudo.', 'Elige un curso en la guía de estudio.'],
  'The course guide could not be loaded.': ['Não foi possível carregar o guia do curso.', 'No se pudo cargar la guía del curso.'],
  'This edition has a plan, but its book has not been written yet.': ['Esta edição tem um plano, mas o livro ainda não foi escrito.', 'Esta edición tiene un plan, pero el libro aún no se ha escrito.'],
  'The book is temporarily unavailable.': ['O livro está temporariamente indisponível.', 'El libro no está disponible temporalmente.'],
  'OPEN REFERENCE': ['REFERÊNCIA ABERTA', 'REFERENCIA ABIERTA'],
  'Course reference': ['Referência do curso', 'Referencia del curso'],
  'Loading the document…': ['Carregando o documento…', 'Cargando el documento…'],
  'Browse courses →': ['Explorar cursos →', 'Explorar cursos →'],
  'Choose a document from a course page.': ['Escolha um documento na página do curso.', 'Elige un documento en la página del curso.'],
  'This reference is unavailable.': ['Esta referência está indisponível.', 'Esta referencia no está disponible.'],
  'Public document · linked course references open within OpenCyber Academy.': ['Documento público · referências do curso abrem no OpenCyber Academy.', 'Documento público · las referencias del curso se abren en OpenCyber Academy.'],
  'LIBRARY FOR AIs': ['BIBLIOTECA PARA IAs', 'BIBLIOTECA PARA IA'],
  'Verifiable knowledge,': ['Conhecimento verificável,', 'Conocimiento verificable,'],
  'accessible by protocol.': ['acessível por protocolo.', 'accesible por protocolo.'],
  'OpenCyber Academy offers the same books to human readers and agents. Discover courses, consult the index and read published chapters. Every result identifies its public source.': ['O OpenCyber Academy oferece os mesmos livros a leitores e agentes. Descubra cursos, consulte o índice e leia capítulos publicados. Cada resultado identifica sua fonte pública.', 'OpenCyber Academy ofrece los mismos libros a lectores y agentes. Descubre cursos, consulta el índice y lee capítulos publicados. Cada resultado identifica su fuente pública.'],
  'Explore lessons ↗': ['Explorar aulas ↗', 'Explorar lecciones ↗'],
  'Open OpenAPI ↗': ['Abrir OpenAPI ↗', 'Abrir OpenAPI ↗'],
  'Connect an agent': ['Conecte um agente', 'Conecta un agente'],
  'Use the public HTTP endpoint in an MCP client that accepts remote servers. Reading books requires no account or key.': ['Use o endpoint HTTP público em um cliente MCP que aceite servidores remotos. Ler livros não exige conta nem chave.', 'Usa el endpoint HTTP público en un cliente MCP que acepte servidores remotos. Leer libros no requiere cuenta ni clave.'],
  'Copy MCP URL': ['Copiar URL MCP', 'Copiar URL MCP'],
  'Copy': ['Copiar', 'Copiar'],
  'Copied': ['Copiado', 'Copiado'],
  'Tools:': ['Ferramentas:', 'Herramientas:'],
  'Resources: catalog and chapters.': ['Recursos: catálogo e capítulos.', 'Recursos: catálogo y capítulos.'],
  'Integrate without an SDK': ['Integre sem SDK', 'Integra sin SDK'],
  'The catalog and each lesson are available as JSON. Complete manuscripts are available as Markdown from the public editorial source.': ['O catálogo e cada aula estão disponíveis em JSON. Manuscritos completos estão disponíveis em Markdown da fonte editorial pública.', 'El catálogo y cada lección están disponibles en JSON. Los manuscritos completos están disponibles en Markdown desde la fuente editorial pública.'],
  'OpenAPI specification →': ['Especificação OpenAPI →', 'Especificación OpenAPI →'],
  'FROM COURSE TO CHAPTER': ['DO CURSO AO CAPÍTULO', 'DEL CURSO AL CAPÍTULO'],
  'Three steps to consult the library.': ['Três passos para consultar a biblioteca.', 'Tres pasos para consultar la biblioteca.'],
  'Discover': ['Descobrir', 'Descubrir'],
  'Locate': ['Localizar', 'Localizar'],
  'Read and cite': ['Ler e citar', 'Leer y citar'],
  'One source, open access.': ['Uma fonte, acesso aberto.', 'Una fuente, acceso abierto.'],
  'List the 207 courses and choose a language, subject and level. The catalog gives the structure; the book is checked again when a lesson opens.': ['Liste os 207 cursos e escolha idioma, tema e nível. O catálogo mostra a estrutura; o livro é verificado quando a aula abre.', 'Consulta los 207 cursos y elige idioma, tema y nivel. El catálogo muestra la estructura; el libro se comprueba al abrir la lección.'],
  'Browse subjects in study order. Each is marked as a published lesson or a planned chapter.': ['Percorra as matérias em ordem de estudo. Cada uma indica aula publicada ou capítulo planejado.', 'Recorre las materias en orden de estudio. Cada una indica lección publicada o capítulo planificado.'],
  'Read the lesson and worked answers. Use its public source URL when citing the original text.': ['Leia a aula e as respostas comentadas. Use a URL da fonte pública ao citar o texto original.', 'Lee la lección y las respuestas desarrolladas. Usa la URL de la fuente pública al citar el texto original.'],
  'The API reads manuscripts from the public': ['A API lê manuscritos da fonte pública', 'La API lee manuscritos de la fuente pública'],
  'branch. Changes to existing books appear without rebuilding the site. The catalog is generated when the site is published; new course structures need a new deployment. A published chapter does not mean the whole book passed editorial review.': ['. Alterações em livros existentes aparecem sem reconstruir o site. O catálogo é gerado na publicação; novas estruturas de curso precisam de novo deploy. Um capítulo publicado não significa que o livro inteiro passou por revisão editorial.', '. Los cambios en libros existentes aparecen sin reconstruir el sitio. El catálogo se genera al publicar; nuevas estructuras de cursos requieren otro despliegue. Un capítulo publicado no significa que el libro completo haya superado la revisión editorial.'],
  'Guide for agents ↗': ['Guia para agentes ↗', 'Guía para agentes ↗'],
  'Usage rights ↗': ['Direitos de uso ↗', 'Derechos de uso ↗'],
  'OPTIONAL STUDENT AREA': ['ÁREA OPCIONAL DO ESTUDANTE', 'ÁREA OPCIONAL DEL ESTUDIANTE'],
  'Your learning,': ['Seu estudo,', 'Tu aprendizaje,'],
  'at your pace.': ['no seu ritmo.', 'a tu ritmo.'],
  'Books, lessons and the API are open without an account. Optional sign-in for saved progress will be added later.': ['Livros, aulas e API estão abertos sem conta. O login opcional para salvar o progresso será adicionado depois.', 'Los libros, las lecciones y la API están abiertos sin cuenta. El inicio de sesión opcional para guardar el progreso se añadirá después.'],
  'IDENTITY': ['IDENTIDADE', 'IDENTIDAD'],
  'Checking access…': ['Verificando acesso…', 'Comprobando acceso…'],
  'YOUR STUDY AREA': ['SUA ÁREA DE ESTUDO', 'TU ÁREA DE ESTUDIO'],
  'Sign-in is managed by Cloudflare Access. OpenCyber Academy does not store your password.': ['O login é gerenciado pelo Cloudflare Access. O OpenCyber Academy não armazena sua senha.', 'El inicio de sesión lo gestiona Cloudflare Access. OpenCyber Academy no guarda tu contraseña.'],
  'What you can track': ['O que você pode acompanhar', 'Qué puedes seguir'],
  'Completed lessons': ['Aulas concluídas', 'Lecciones completadas'],
  'Mark a chapter when you finish reading.': ['Marque um capítulo ao terminar a leitura.', 'Marca un capítulo cuando termines de leer.'],
  'Exercise attempts': ['Tentativas de exercícios', 'Intentos de ejercicios'],
  'Save your answers and continue later.': ['Salve suas respostas e continue depois.', 'Guarda tus respuestas y continúa después.'],
  'Audio and video': ['Áudio e vídeo', 'Audio y vídeo'],
  'Planned for a later stage; reading is already open.': ['Planejado para uma etapa futura; a leitura já está aberta.', 'Previsto para una etapa futura; la lectura ya está abierta.'],
  'MY HISTORY': ['MEU HISTÓRICO', 'MI HISTORIAL'],
  'Saved progress': ['Progresso salvo', 'Progreso guardado'],
  'Sign in to view your lessons and attempts.': ['Entre para ver suas aulas e tentativas.', 'Inicia sesión para ver tus lecciones e intentos.'],
  'Continue learning →': ['Continuar estudando →', 'Seguir estudiando →'],
  'Sign in with email →': ['Entrar com e-mail →', 'Iniciar sesión con correo →'],
  'Study without an account →': ['Estudar sem conta →', 'Estudiar sin cuenta →'],
  'Optional sign-in is not enabled on this domain yet.': ['O login opcional ainda não está ativado neste domínio.', 'El inicio de sesión opcional aún no está habilitado en este dominio.'],
  'Sign in to save progress.': ['Entre para salvar o progresso.', 'Inicia sesión para guardar el progreso.'],
  'Active session': ['Sessão ativa', 'Sesión activa'],
  'Your progress belongs only to your account.': ['Seu progresso pertence somente à sua conta.', 'Tu progreso pertenece solo a tu cuenta.'],
  'Progress could not be loaded now.': ['Não foi possível carregar o progresso agora.', 'No se pudo cargar el progreso ahora.'],
  'Completed': ['Concluída', 'Completada'],
  'In progress': ['Em andamento', 'En curso'],
  'No lessons marked yet. Begin with a published lesson.': ['Nenhuma aula marcada ainda. Comece por uma aula publicada.', 'Aún no hay lecciones marcadas. Comienza con una lección publicada.'],
  'Reading always open': ['Leitura sempre aberta', 'Lectura siempre abierta'],
  'Your history will appear when optional sign-in is available and you sign in.': ['Seu histórico aparecerá quando o login opcional estiver disponível e você entrar.', 'Tu historial aparecerá cuando el inicio de sesión opcional esté disponible y entres.'],
};

function dynamic(english: string, lang: Exclude<Language, 'en'>): string | null {
  const chapterLessons = english.match(/^([A-Z]{2}) · (\d+) chapter-lessons$/);
  if (chapterLessons) return lang === 'pt' ? `${chapterLessons[1]} · ${chapterLessons[2]} capítulos-aula` : `${chapterLessons[1]} · ${chapterLessons[2]} capítulos-lección`;
  const editionSummary = english.match(/^([A-Z]{2}) · (\d+) daily lessons · (\d+) full chapters$/);
  if (editionSummary) return lang === 'pt' ? `${editionSummary[1]} · ${editionSummary[2]} aulas diárias · ${editionSummary[3]} capítulos completos` : `${editionSummary[1]} · ${editionSummary[2]} lecciones diarias · ${editionSummary[3]} capítulos completos`;
  const directoryUnit = english.match(/^(Lesson|Chapter) (\d+):$/);
  if (directoryUnit) return `${directoryUnit[1] === 'Lesson' ? (lang === 'pt' ? 'Aula' : 'Lección') : 'Capítulo'} ${directoryUnit[2]}:`;
  const plannedCadence = english.match(/^(\d+) weeks · (\d+) planned daily lessons$/);
  if (plannedCadence) return lang === 'pt' ? `${plannedCadence[1]} semanas · ${plannedCadence[2]} aulas diárias previstas` : `${plannedCadence[1]} semanas · ${plannedCadence[2]} lecciones diarias previstas`;
  const chapterLessonFraction = english.match(/^(\d+)(?: of |\/)(\d+) chapter-lessons written$/);
  if (chapterLessonFraction) return lang === 'pt' ? `${chapterLessonFraction[1]} de ${chapterLessonFraction[2]} capítulos-aula escritos` : `${chapterLessonFraction[1]} de ${chapterLessonFraction[2]} capítulos-lección escritos`;
  const chapterLessonEdition = english.match(/^(\d+) chapter-lessons are published in this edition\.$/);
  if (chapterLessonEdition) return lang === 'pt' ? `${chapterLessonEdition[1]} capítulos-aula publicados nesta edição.` : `${chapterLessonEdition[1]} capítulos-lección publicados en esta edición.`;
  const writtenFraction = english.match(/^(\d+)\/(\d+) daily lessons written$/);
  if (writtenFraction) return lang === 'pt' ? `${writtenFraction[1]}/${writtenFraction[2]} aulas diárias escritas` : `${writtenFraction[1]}/${writtenFraction[2]} lecciones diarias escritas`;
  const courseEdition = english.match(/^(\d+) daily lessons and (\d+) chapters are published in this edition\.$/);
  if (courseEdition) return lang === 'pt' ? `${courseEdition[1]} aulas diárias e ${courseEdition[2]} capítulos publicados nesta edição.` : `${courseEdition[1]} lecciones diarias y ${courseEdition[2]} capítulos publicados en esta edición.`;
  const chapterEdition = english.match(/^(\d+) chapters are published in this edition\. Daily study slots are a plan\.$/);
  if (chapterEdition) return lang === 'pt' ? `${chapterEdition[1]} capítulos publicados nesta edição. Os dias de estudo são apenas um plano.` : `${chapterEdition[1]} capítulos publicados en esta edición. Los días de estudio son solo un plan.`;
  const linkedExercises = english.match(/^(\d+) linked exercises · (Worked answers available|Worked answer pending)$/);
  if (linkedExercises) return lang === 'pt' ? `${linkedExercises[1]} exercícios vinculados · ${linkedExercises[2] === 'Worked answers available' ? 'Respostas comentadas disponíveis' : 'Resposta comentada pendente'}` : `${linkedExercises[1]} ejercicios vinculados · ${linkedExercises[2] === 'Worked answers available' ? 'Respuestas desarrolladas disponibles' : 'Respuesta desarrollada pendiente'}`;
  const weekStatus = english.match(/^Week (\d{2}) · (\d+)\/(\d+) written$/);
  if (weekStatus) return lang === 'pt' ? `Semana ${weekStatus[1]} · ${weekStatus[2]}/${weekStatus[3]} escritas` : `Semana ${weekStatus[1]} · ${weekStatus[2]}/${weekStatus[3]} escritas`;
  const weekHeading = english.match(/^Week (\d{2})(?: · (.+))?$/);
  if (weekHeading) return `Semana ${weekHeading[1]}${weekHeading[2] ? ` · ${weekHeading[2]}` : ''}`;
  const dailyAndChapters = english.match(/^(\d+) of (\d+) daily lessons written · (\d+) existing subject chapters readable$/);
  if (dailyAndChapters) return lang === 'pt' ? `${dailyAndChapters[1]} de ${dailyAndChapters[2]} aulas diárias escritas · ${dailyAndChapters[3]} capítulos de matérias disponíveis` : `${dailyAndChapters[1]} de ${dailyAndChapters[2]} lecciones diarias escritas · ${dailyAndChapters[3]} capítulos de materias disponibles`;
  const writtenDaily = english.match(/^(\d+) of (\d+) daily lessons written$/);
  if (writtenDaily) return lang === 'pt' ? `${writtenDaily[1]} de ${writtenDaily[2]} aulas diárias escritas` : `${writtenDaily[1]} de ${writtenDaily[2]} lecciones diarias escritas`;
  const fullChapters = english.match(/^Browse all (\d+) full chapters$/);
  if (fullChapters) return lang === 'pt' ? `Explore os ${fullChapters[1]} capítulos completos` : `Explora los ${fullChapters[1]} capítulos completos`;
  const studyWeeks = english.match(/^(\d+) study weeks$/);
  if (studyWeeks) return lang === 'pt' ? `${studyWeeks[1]} semanas de estudo` : `${studyWeeks[1]} semanas de estudio`;
  const readableChapters = english.match(/^(\d+) chapters readable$/);
  if (readableChapters) return lang === 'pt' ? `${readableChapters[1]} capítulos disponíveis` : `${readableChapters[1]} capítulos disponibles`;
  const chapterLessonPosition = english.match(/^Chapter (\d+) · (.+) · Lesson (\d+) of (\d+)$/);
  if (chapterLessonPosition) return `${lang === 'pt' ? 'Capítulo' : 'Capítulo'} ${chapterLessonPosition[1]} · ${chapterLessonPosition[2]} · ${lang === 'pt' ? 'Aula' : 'Lección'} ${chapterLessonPosition[3]} de ${chapterLessonPosition[4]}`;
  const chapterLabel = english.match(/^Chapter (\d+) · (.+)$/);
  if (chapterLabel) return `Capítulo ${chapterLabel[1]} · ${chapterLabel[2]}`;
  const weeklyChapters = english.match(/^(\d+) weekly chapters planned$/);
  if (weeklyChapters) return lang === 'pt' ? `${weeklyChapters[1]} capítulos semanais previstos` : `${weeklyChapters[1]} capítulos semanales previstos`;
  const chaptersPublished = english.match(/^(\d+) chapters published$/);
  if (chaptersPublished) return `${chaptersPublished[1]} capítulos publicados`;
  const lessonsPublished = english.match(/^(\d+) daily lessons published$/);
  if (lessonsPublished) return lang === 'pt' ? `${lessonsPublished[1]} aulas diárias publicadas` : `${lessonsPublished[1]} lecciones diarias publicadas`;
  const chapterAvailability = english.match(/^(\d+) chapters and (\d+) of (\d+) indexed daily lessons published in this edition\.$/);
  if (chapterAvailability) return lang === 'pt' ? `${chapterAvailability[1]} capítulos e ${chapterAvailability[2]} de ${chapterAvailability[3]} aulas diárias indexadas publicados nesta edição.` : `${chapterAvailability[1]} capítulos y ${chapterAvailability[2]} de ${chapterAvailability[3]} lecciones diarias indexadas publicados en esta edición.`;
  const legacyChapterAvailability = english.match(/^(\d+) current subject chapters published\. Distinct daily lessons have not yet been indexed for this edition; the (\d+)-lesson baseline is a plan, not published content\.$/);
  if (legacyChapterAvailability) return lang === 'pt' ? `${legacyChapterAvailability[1]} capítulos antigos de matérias publicados. Aulas diárias distintas ainda não foram indexadas nesta edição; a base de ${legacyChapterAvailability[2]} aulas é um plano, não conteúdo publicado.` : `${legacyChapterAvailability[1]} capítulos anteriores de materias publicados. Aún no se han indexado lecciones diarias distintas en esta edición; la base de ${legacyChapterAvailability[2]} lecciones es un plan, no contenido publicado.`;
  const dailyIntro = english.match(/^(\d+) chapters and (\d+) daily lessons are published in this edition\.$/);
  if (dailyIntro) return lang === 'pt' ? `${dailyIntro[1]} capítulos e ${dailyIntro[2]} aulas diárias estão publicados nesta edição.` : `${dailyIntro[1]} capítulos y ${dailyIntro[2]} lecciones diarias están publicados en esta edición.`;
  const legacyIntro = english.match(/^(\d+) legacy subject chapters are published\. The daily lessons are still being developed\.$/);
  if (legacyIntro) return lang === 'pt' ? `${legacyIntro[1]} capítulos antigos de matérias estão publicados. As aulas diárias ainda estão em desenvolvimento.` : `${legacyIntro[1]} capítulos anteriores de materias están publicados. Las lecciones diarias siguen en desarrollo.`;
  const bookDaily = english.match(/^(\d+) written chapters · (\d+) daily lessons · Read here or choose one lesson from the guide\.$/);
  if (bookDaily) return lang === 'pt' ? `${bookDaily[1]} capítulos escritos · ${bookDaily[2]} aulas diárias · Leia aqui ou escolha uma aula no guia.` : `${bookDaily[1]} capítulos escritos · ${bookDaily[2]} lecciones diarias · Lee aquí o elige una lección de la guía.`;
  const bookLegacy = english.match(/^(\d+) legacy subject chapters · Read here or open the course guide\.$/);
  if (bookLegacy) return lang === 'pt' ? `${bookLegacy[1]} capítulos antigos de matérias · Leia aqui ou abra o guia do curso.` : `${bookLegacy[1]} capítulos anteriores de materias · Lee aquí o abre la guía del curso.`;
  const bareModule = english.match(/^Module (\d+)$/);
  if (bareModule) return `Módulo ${bareModule[1]}`;
  const weeks = english.match(/^(\d+) instructional weeks$/);
  if (weeks) return lang === 'pt' ? `${weeks[1]} semanas letivas` : `${weeks[1]} semanas lectivas`;
  const target = english.match(/^(\d+) daily lessons planned$/);
  if (target) return lang === 'pt' ? `${target[1]} aulas diárias previstas` : `${target[1]} lecciones diarias previstas`;
  const current = english.match(/^(\d+) current chapters published$/);
  if (current) return lang === 'pt' ? `${current[1]} capítulos atuais publicados` : `${current[1]} capítulos actuales publicados`;
  const publishedLessons = english.match(/^(\d+) lessons published$/);
  if (publishedLessons) return lang === 'pt' ? `${publishedLessons[1]} aulas publicadas` : `${publishedLessons[1]} lecciones publicadas`;
  const publishedNote = english.match(/^(\d+) lessons published in this edition\. An outline is not a lesson\.$/);
  if (publishedNote) return lang === 'pt' ? `${publishedNote[1]} aulas publicadas nesta edição. Um plano não é uma aula.` : `${publishedNote[1]} lecciones publicadas en esta edición. Un plan no es una lección.`;
  const publishedMinimum = english.match(/^(\d+) lessons published in this edition\. Planning minimum: (\d+)\. An outline is not a lesson\.$/);
  if (publishedMinimum) return lang === 'pt' ? `${publishedMinimum[1]} aulas publicadas nesta edição. Mínimo de planejamento: ${publishedMinimum[2]}. Um plano não é uma aula.` : `${publishedMinimum[1]} lecciones publicadas en esta edición. Mínimo de planificación: ${publishedMinimum[2]}. Un plan no es una lección.`;
  const planningMinimum = english.match(/^Planning minimum (\d+)$/);
  if (planningMinimum) return lang === 'pt' ? `Mínimo de planejamento ${planningMinimum[1]}` : `Mínimo de planificación ${planningMinimum[1]}`;
  const indexWithMinimum = english.match(/^(\d+) chapters in the current index · minimum (\d+)$/);
  if (indexWithMinimum) return lang === 'pt' ? `${indexWithMinimum[1]} capítulos no índice atual · mínimo ${indexWithMinimum[2]}` : `${indexWithMinimum[1]} capítulos en el índice actual · mínimo ${indexWithMinimum[2]}`;
  const indexChapters = english.match(/^(\d+) chapters in the current index$/);
  if (indexChapters) return lang === 'pt' ? `${indexChapters[1]} capítulos no índice atual` : `${indexChapters[1]} capítulos en el índice actual`;
  const directoryTarget = english.match(/^(\d+) weekday lessons planned · (\d+) current curriculum chapters$/);
  if (directoryTarget) return lang === 'pt' ? `${directoryTarget[1]} aulas por dia útil previstas · ${directoryTarget[2]} capítulos curriculares atuais` : `${directoryTarget[1]} lecciones por día hábil previstas · ${directoryTarget[2]} capítulos curriculares actuales`;
  const weeklyTitle = english.match(/^(\d+) weeks · (\d+) daily lessons$/);
  if (weeklyTitle) return lang === 'pt' ? `${weeklyTitle[1]} semanas · ${weeklyTitle[2]} aulas diárias` : `${weeklyTitle[1]} semanas · ${weeklyTitle[2]} lecciones diarias`;
  const dailyAvailability = english.match(/^(\d+) of (\d+) daily chapters published in this edition\. Unpublished lessons are not available yet\.$/);
  if (dailyAvailability) return lang === 'pt' ? `${dailyAvailability[1]} de ${dailyAvailability[2]} capítulos diários publicados nesta edição. Aulas não publicadas ainda não estão disponíveis.` : `${dailyAvailability[1]} de ${dailyAvailability[2]} capítulos diarios publicados en esta edición. Las lecciones no publicadas aún no están disponibles.`;
  const legacyAvailability = english.match(/^(\d+) current chapters published\. These older subject chapters are not yet the (\d+) distinct daily lessons required by the new schedule\.$/);
  if (legacyAvailability) return lang === 'pt' ? `${legacyAvailability[1]} capítulos atuais publicados. Esses capítulos antigos de matérias ainda não são as ${legacyAvailability[2]} aulas diárias distintas exigidas pelo novo plano.` : `${legacyAvailability[1]} capítulos actuales publicados. Estos capítulos antiguos de materias aún no son las ${legacyAvailability[2]} lecciones diarias distintas exigidas por el nuevo plan.`;
  const introLegacy = english.match(/^(\d+) current chapters are published\. Daily chapters are being developed toward the (\d+)-lesson target\.$/);
  if (introLegacy) return lang === 'pt' ? `${introLegacy[1]} capítulos atuais publicados. As aulas diárias estão em desenvolvimento rumo à meta de ${introLegacy[2]}.` : `${introLegacy[1]} capítulos actuales publicados. Las lecciones diarias están en desarrollo hacia la meta de ${introLegacy[2]}.`;
  const module = english.match(/^Module (\d+) · (Week|Month|Semester|Term|Year|Module) \d+$/);
  if (module) {
    const names: Record<string, [string, string]> = { Week: ['Semana', 'Semana'], Month: ['Mês', 'Mes'], Semester: ['Semestre', 'Semestre'], Term: ['Período', 'Período'], Year: ['Ano', 'Año'], Module: ['Módulo', 'Módulo'] };
    const kind = names[module[2]][lang === 'pt' ? 0 : 1];
    return `${lang === 'pt' ? 'Módulo' : 'Módulo'} ${module[1]} · ${kind} ${module[1]}`;
  }
  const moduleLesson = english.match(/^Module (\d+) · (Week|Month|Semester|Term|Year|Module) \d+ · Lesson (\d+) of (\d+)$/);
  if (moduleLesson) {
    const label = dynamic(`Module ${moduleLesson[1]} · ${moduleLesson[2]} ${moduleLesson[1]}`, lang);
    return `${label} · ${lang === 'pt' ? 'Aula' : 'Lección'} ${moduleLesson[3]} ${lang === 'pt' ? 'de' : 'de'} ${moduleLesson[4]}`;
  }
  const simpleLesson = english.match(/^Lesson (\d+) of (\d+)$/);
  if (simpleLesson) return lang === 'pt' ? `Aula ${simpleLesson[1]} de ${simpleLesson[2]}` : `Lección ${simpleLesson[1]} de ${simpleLesson[2]}`;
  const moduleCount = english.match(/^(\d+) modules$/);
  if (moduleCount) return `${moduleCount[1]} módulos`;
  const lessonCount = english.match(/^(\d+) lessons$/);
  if (lessonCount) return lang === 'pt' ? `${lessonCount[1]} aulas` : `${lessonCount[1]} lecciones`;
  const availableCount = english.match(/^(\d+) lessons available$/);
  if (availableCount) return lang === 'pt' ? `${availableCount[1]} aulas disponíveis` : `${availableCount[1]} lecciones disponibles`;
  const availableModule = english.match(/^(\d+) of (\d+) lessons available$/);
  if (availableModule) return lang === 'pt' ? `${availableModule[1]} de ${availableModule[2]} aulas disponíveis` : `${availableModule[1]} de ${availableModule[2]} lecciones disponibles`;
  const exerciseCount = english.match(/^(\d+) exercises · Worked answers below$/);
  if (exerciseCount) return lang === 'pt' ? `${exerciseCount[1]} exercícios · Respostas comentadas abaixo` : `${exerciseCount[1]} ejercicios · Respuestas desarrolladas abajo`;
  const levelDirectory = english.match(/^LEVEL (\d{2}) · 23 COURSES$/);
  if (levelDirectory) return lang === 'pt' ? `NÍVEL ${levelDirectory[1]} · 23 CURSOS` : `NIVEL ${levelDirectory[1]} · 23 CURSOS`;
  const subjectDirectory = english.match(/^SUBJECT · 9 SEPARATE COURSES$/);
  if (subjectDirectory) return lang === 'pt' ? 'TEMA · 9 CURSOS SEPARADOS' : 'TEMA · 9 CURSOS SEPARADOS';
  const levelCourse = english.match(/^LEVEL (\d{2}) · COURSE (\d{3})$/);
  if (levelCourse) return lang === 'pt' ? `NÍVEL ${levelCourse[1]} · CURSO ${levelCourse[2]}` : `NIVEL ${levelCourse[1]} · CURSO ${levelCourse[2]}`;
  const numbering = english.match(/^(LEVEL|COURSE|SUBJECT) (\d{2,3})( ·)?$/);
  if (numbering) return `${({ LEVEL: lang === 'pt' ? 'NÍVEL' : 'NIVEL', COURSE: 'CURSO', SUBJECT: 'TEMA' } as Record<string, string>)[numbering[1]]} ${numbering[2]}${numbering[3] || ''}`;
  const plannedLessons = english.match(/^(\d+) lessons in (?:the course guide|this course)$/);
  if (plannedLessons) return lang === 'pt' ? `${plannedLessons[1]} aulas neste curso` : `${plannedLessons[1]} lecciones en este curso`;
  const answer = english.match(/^Your answer for (EX\d+)$/);
  if (answer) return lang === 'pt' ? `Sua resposta para ${answer[1]}` : `Tu respuesta para ${answer[1]}`;
  const book = english.match(/^(\d+) written chapters · Read here or choose one lesson from the guide\.$/);
  if (book) return lang === 'pt' ? `${book[1]} capítulos escritos · Leia aqui ou escolha uma aula no guia.` : `${book[1]} capítulos escritos · Lee aquí o elige una lección de la guía.`;
  const published = english.match(/^(\d+) of (\d+) chapters have published lesson text in this edition\. A planned chapter may not yet have a lesson\.$/);
  if (published) return lang === 'pt' ? `${published[1]} de ${published[2]} capítulos têm aulas publicadas nesta edição. Um capítulo planejado pode ainda não ter aula.` : `${published[1]} de ${published[2]} capítulos tienen lecciones publicadas en esta edición. Un capítulo planificado puede no tener aún lección.`;
  const loaded = english.match(/^Guide updated for (.+)\.$/);
  if (loaded) return lang === 'pt' ? `Guia atualizado para ${loaded[1]}.` : `Guía actualizada para ${loaded[1]}.`;
  const lesson = english.match(/^Lesson (\d+) loaded from the public book\.$/);
  if (lesson) return lang === 'pt' ? `Aula ${lesson[1]} carregada do livro público.` : `Lección ${lesson[1]} cargada del libro público.`;
  const exercises = english.match(/^(\d+) exercise\(s\) found in this lesson · Public book edition$/);
  if (exercises) return lang === 'pt' ? `${exercises[1]} exercício(s) nesta aula · Edição pública do livro` : `${exercises[1]} ejercicio(s) en esta lección · Edición pública del libro`;
  return null;
}

export function ui(english: string): string {
  const pair = copy[english];
  const lang = siteLanguage();
  const subject = subjectTitles[english];
  return lang === 'en' ? english : subject ? subject[lang] : pair ? pair[lang === 'pt' ? 0 : 1] : dynamic(english, lang) || english;
}

function translateText(node: Text): void {
  const parent = node.parentElement;
  if (!parent || parent.closest('.prose, script, style, pre, code')) return;
  const raw = node.textContent || '';
  const value = raw.trim();
  if (!value) return;
  const translated = ui(value);
  if (translated !== value) node.textContent = raw.replace(value, translated);
}

function translateNode(root: Node): void {
  if (root.nodeType === Node.TEXT_NODE) { translateText(root as Text); return; }
  if (!(root instanceof Element)) return;
  if (root.closest('.prose, script, style, pre, code')) return;
  for (const name of ['aria-label', 'title', 'placeholder']) {
    const original = root.getAttribute(name);
    if (original) root.setAttribute(name, ui(original));
  }
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  for (let current = walker.nextNode(); current; current = walker.nextNode()) translateText(current as Text);
  for (const element of root.querySelectorAll('[aria-label], [title], [placeholder]')) {
    for (const name of ['aria-label', 'title', 'placeholder']) {
      const original = element.getAttribute(name);
      if (original) element.setAttribute(name, ui(original));
    }
  }
}

export function translatePage(): void {
  if (siteLanguage() === 'en') return;
  translateNode(document.body);
  new MutationObserver(records => {
    for (const record of records) {
      if (record.type === 'characterData') translateNode(record.target);
      else for (const node of record.addedNodes) translateNode(node);
    }
  }).observe(document.body, { childList: true, characterData: true, subtree: true });
}
