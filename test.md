# html to markdown: 80389 -> 26592 -> 26592 (compressed)
GraphRAG vs LightRAG en 2025: Adaptive RAG con GPT-5-nano (caso real UAB)
=========================================================================

[<img src='https://miro.medium.com/v2/resize:fill:64:64/1*NGrTWg_ruO-u00-7rWX71w.jpeg' alt='Albert Gil López' title='' width='32' height='32' />](/@jddam?source=post_page---byline--97e3ce509fba---------------------------------------)[Albert Gil López](/@jddam?source=post_page---byline--97e3ce509fba---------------------------------------)Follow

12 min read·6 days agoShare

More

Press enter or click to view image in full size<img src='https://miro.medium.com/v2/resize:fit:1400/1*gTm6-w2b9WSqwHcUHsIaQA.png' alt='' title='' width='700' height='700' />

*AUTOR: GPT-5*

En 2025, el ecosistema de **Retrieval-Augmented Generation (RAG)** ha evolucionado hacia un escenario mucho más sofisticado y competitivo. Entre las múltiples propuestas, dos librerías destacan por su madurez y adopción en producción: **GraphRAG de Microsoft** y **LightRAG de la HKU**. A su alrededor aparecen nuevas alternativas como **LazyGraphRAG**, **MiniRAG** o **RAG-Anything**, que amplían el abanico de posibilidades pero también hacen más compleja la elección.

El reto es mapear las capacidades de **17 grupos de investigación de la Escuela de Ingeniería de la Universidad Autónoma de Barcelona (UAB)** y responder tanto a **consultas factuales inmediatas** *(“¿Qué es SPCOMNAV?”)* como a **análisis estratégicos complejos** *(“¿Qué oportunidades de colaboración existen entre departamentos?”).*

La solución fue diseñar un sistema [**Adaptive RAG**](https://arxiv.org/abs/2403.14403)capaz de **seleccionar dinámicamente** entre GraphRAG y LightRAG en función de la complejidad de cada consulta. Para ello, integramos un *router* inteligente basado en el recién lanzado **GPT-5-nano** ($0.05/1M tokens), optimizado para tareas de clasificación masiva con latencias muy bajas.

**RESULTADO:** 100% de fiabilidad, un coste de apenas **$0.00136 por consulta** y tiempos de decisión de *routing* de solo **2–3 segundos**, combinando lo mejor de ambos mundos sin sacrificar velocidad ni profundidad analítica.

Background: Las 8 Arquitecturas RAG en 2025
===========================================

Antes de profundizar en GraphRAG y LightRAG, es crucial entender dónde se sitúan en el panorama actual de arquitecturas RAG:

Press enter or click to view image in full size<img src='https://miro.medium.com/v2/resize:fit:1400/1*4zYEgz35txWLa8DejrjcxQ.jpeg' alt='' title='' width='700' height='819' />

**Fuente:* [*@_avichawla*](https://x.com/_avichawla/status/1956241967136039197)*

1. Naive RAG
------------

* Arquitectura básica: *retrieve → augment → generate*
* Simple pero efectiva para FAQ y documentación estática (pequeños conjuntos de datos)
* Limita con preguntas complejas o gran volumen de información (sin razonamiento adicional)

2. Multimodal RAG
-----------------

* Procesa texto, imágenes, audio y video simultáneamente
* Esencial para aplicaciones que requieren comprensión *cross-modal*

3. HyDE (Hypothetical Document Embeddings)
------------------------------------------

* Genera documentos hipotéticos antes de recuperar
* Útil para *queries* vagas o exploratorias (amplía el contexto de búsqueda)

4. Corrective RAG (CRAG)
------------------------

* Autoevaluación y corrección de documentos recuperados
* Ideal para dominios que requieren alta precisión (legal, médico)

5. Graph RAG ⭐
--------------

* **Aquí se sitúa Microsoft GraphRAG**
* Convierte contenido en grafos de conocimiento
* Captura relaciones complejas entre entidades
* Excelente para análisis holístico y *“connecting the dots”*

6. Hybrid RAG ⭐
---------------

* **Aquí se sitúa LightRAG de HKU**
* Combina búsqueda vectorial + grafo + *naive* simultáneamente
* LightRAG en modo “hybrid” fusiona 3 métodos en paralelo: Local search (entidades específicas), Global search (conceptos amplios) y Naive search (chunks de texto)
* Fusiona y reordena resultados de múltiples fuentes

7. Adaptive RAG ⭐
-----------------

* **Aquí se sitúa nuestro sistema con el router que utiliza GPT-5-nano**
* Ajusta la estrategia según complejidad de la *query*
* No fusiona, sino que **selecciona** entre sistemas completos
* Decide dinámicamente:

*Queries simples → LightRAG (Hybrid RAG)  
Queries complejas → GraphRAG (Graph RAG)*

8. Agentic RAG
--------------

* Agentes autónomos que orquestan múltiples fuentes
* Planificación, razonamiento y memoria para tareas complejas
* Combina lo mejor de RAG con agentes de IA

GraphRAG (Microsoft Research)
-----------------------------

Lanzado en julio 2024 y actualizado a v1.0 en diciembre 2024, GraphRAG es el framework de Microsoft que ha cambiado el paradigma del RAG tradicional mediante *clustering* jerárquico de comunidades para como mencionan ellos: *“unlock LLM discovery on narrative private data”*.

Está basado en el **algoritmo Leiden,** una mejora del algoritmo Louvain desarrollada en la Universidad de Leiden. Su función es detectar **comunidades** *(grupos de nodos densamente conectados)* en grafos grandes.

Funciona en tres fases:

1. Mueve nodos entre comunidades para maximizar la modularidad.
2. Se asegura que cada comunidad esté bien conectada internamente *(ventaja sobre Louvain, que puede crear comunidades desconectadas).*
3. Colapsa comunidades en super-nodos y repite el proceso.

El **clustering jerárquico** significa que GraphRAG crea múltiples niveles de abstracción. En nuestro caso de uso:

* **Nivel 0**: Entidades individuales (ej: “SPCOMNAV”, “Dr. García”).
* **Nivel 1**: Comunidades pequeñas (ej: “Grupos de Telecomunicaciones”).
* **Nivel 2**: Comunidades mayores (ej: “Investigación en Ingeniería”).
* **Nivel N**: Vista global del dataset completo.

GraphRAG utiliza este pipeline en 4 fases:

**1. Ingestion Layer**:

* Divide documentos en *chunks* de ~300 tokens.
* Extrae metadatos y prepara el contenido para procesamiento.

**2. Graph Construction Layer**:

* Un LLM extrae entidades y relaciones de cada *chunk*.
* Construye un grafo inicial con todas las conexiones detectadas.
* Aplica Leiden para detectar comunidades jerárquicas.

**3. Retrieval Layer**:

* Para *queries* locales: busca entidades específicas en el grafo.
* Para *queries* globales: navega la jerarquía de comunidades.
* Selecciona el nivel de abstracción apropiado según el alcance de la pregunta.

**4. Generation Layer**:

* Sintetiza información de múltiples fuentes (nodos y comunidades relevantes).
* Genera una respuesta coherente usando *summaries* de comunidad.

Los **community summaries** son resúmenes automáticos generados por el LLM para cada comunidad detectada, facilitando respuestas globales sin recorrer todo el dataset cada vez:

```
  
# Ejemplo simplificado del proceso de resumen comunitario  
for community in detected_communities:  
    entities = get_entities_in_community(community)  
    relationships = get_relationships(entities)  
      
    summary_prompt = f"""  
    Summarize this community of {len(entities)} entities:  
    Entities: {entities}  
    Relationships: {relationships}  
    Create a coherent summary of what this group represents.  
    """  
      
    community.summary = llm.generate(summary_prompt)
```
Esto permite a GraphRAG responder preguntas globales aprovechando resúmenes precomputados de cada comunidad, en lugar de procesar todo el dataset en cada consulta.

Ahora, las queries son relativamente **lentas** (30–40 segundos por consulta) debido a que debe atravesar **múltiples niveles de la jerarquía de grafos** y **combinar información de múltiples comunidades** antes de contestar.

Además, **cada nivel puede requerir procesamiento adicional con el LLM** (p.e. para generar resúmenes), sin olvidar la **complejidad computacional** de las operaciones *~O(n log n)* para grafos grandes.

LightRAG (University of Hong Kong)
----------------------------------

Publicado en octubre 2024 [(arXiv:2410.05779)](https://arxiv.org/abs/2410.05779), LightRAG propone *“Simple and Fast Retrieval-Augmented Generation”*. Es una implementación de una arquitectura **Hybrid RAG** que **fusiona** múltiples métodos de búsqueda en paralelo mediante un sistema de recuperación de dos niveles.

LightRAG implementa dos niveles de recuperación que operan simultáneamente:

**1. Low-Level Retrieval (Recuperación de Bajo Nivel).** Recuperar entidades específicas y sus atributos directos mediante una búsqueda vectorial directa + extracción de nodos específicos del grafo.

**Ejemplo**: *Query* “¿Qué es SPCOMNAV?” → Busca el nodo *SPCOMNAV* en el grafo + relaciones inmediatas asociadas. ~O(log n) usando índices vectoriales eficientes (FAISS u otro motor de similitud).

**2. High-Level Retrieval (Recuperación de Alto Nivel).** Sintetizar temas y conceptos amplios relacionados con la consulta madiante navegación por clusters de nodos relacionados temáticamente.

**Ejemplo**: *Query* “tendencias en investigación” → Atraviesa clusters temáticos en el grafo (ej: grupos de temas de investigación) para identificar tendencias globales. ~O(k · log n) donde *k* es el número de clusters relevantes explorados.

LightRAG ofrece cuatro modos de operación configurables:

```
  
# Ejemplos de modos de consulta en LightRAG  
rag.query(query, mode="local")    # Solo búsqueda de entidades específicas (low-level)  
rag.query(query, mode="global")   # Solo búsqueda de conceptos amplios (high-level)  
rag.query(query, mode="naive")    # Solo búsqueda en chunks de texto planos  
rag.query(query, mode="hybrid")   # FUSIÓN de los 3 anteriores (por defecto)  
  
# Proceso simplificado del modo "hybrid" (Hybrid RAG)  
def hybrid_retrieval(query):  
  
    # Ejecuta los 3 métodos en PARALELO  
    local_results = local_search(query)    # Low-level entities  
    global_results = global_search(query)  # High-level concepts  
    naive_results = naive_search(query)    # Text chunks  
      
    # Fusiona y reordena todos los resultados  
    all_results = local_results + global_results + naive_results  
    return merge_and_rank(all_results)
```
**Por esto LightRAG es *Hybrid RAG***: no elige un método u otro, sino que **fusiona múltiples métodos simultáneamente** para aprovechar lo mejor de cada uno.

A diferencia de GraphRAG, que suele requerir reconstruir todo el índice de grafos ante cualquier cambio, LightRAG permite **actualización incremental** de su índice:

```
  
# Proceso de actualización incremental en LightRAG  
def incremental_update(new_document):  
  
    # 1. Extrae nuevas entidades y relaciones del documento  
    new_entities = extract_entities(new_document)  
    new_relations = extract_relations(new_document)  
      
    # 2. Deduplica contra el índice existente  
    unique_entities = deduplicate(new_entities, existing_entities)  
      
    # 3. Solo indexa lo nuevo (NO reconstruye todo desde cero)  
    if unique_entities:  
        entity_index.add(unique_entities)            # O(m) donde m = nuevas entidades  
        update_vector_embeddings(unique_entities)    # Actualiza embeddings  
      
    # 4. Actualiza grafo localmente con nuevos nodos/aristas  
    graph.add_nodes(unique_entities)  
    graph.add_edges(new_relations)  
      
    # Total: O(m) vs O(n) de reconstrucción completa
```
Otra ventaja es que LightRAG logra latencias de **20–100 ms** por consulta gracias a:

**1. Sin Navegación Jerárquica**:

* Acceso directo a entidades vía índice vectorial optimizado.
* No atraviesa múltiples niveles como GraphRAG, reduciendo pasos intermedios.

**2. Búsqueda Vectorial Optimizada**:

* Usa estructuras como FAISS para búsqueda aproximada en O(log n) con miles de embeddings.
* Índices precomputados en memoria evitan cálculos repetitivos.

**3. Grafo Local, No Global**:

* Solo explora vecinos inmediatos (*1-hop neighbors*) en el grafo alrededor de entidades relevantes.
* No requiere consolidar información de comunidades lejanas ni generar resúmenes globales costosos.

**4. Sin LLM en el *Critical Path***:

* El LLM solo se usa para generar la respuesta final (síntesis), **no** para la etapa de búsqueda o navegación.
* A diferencia de GraphRAG, no hay múltiples llamadas al LLM durante la recuperación, solo al final para formulación de la respuesta.

EXTRA — Event Loop: Issue Conocido
----------------------------------

Un error conocido *“Event loop is closed”* está reportado en GitHub *(*[*Issue #209*](https://github.com/HKUDS/LightRAG/issues/209)*)* y afecta principalmente a entornos Windows al usar LightRAG.

* LightRAG usa `asyncio` para paralelización. En Windows, el `ProactorEventLoop` tiene problemas al cerrarse, y las tareas pendientes no se cancelan correctamente, cerrando el loop de evento inesperadamente tras la primera consulta.
* **Solución 1:** Cambiar la política de event loop en Windows antes de usar LightRAG.

```
import asyncio asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```
* **Solución 2:** Usar `nest_asyncio` para permitir reusar el loop.

```
import nest_asyncio nest_asyncio.apply()
```
* **Solución 3:** Utilizar un *wrapper* que implementamos que garantiza el 100% de fiabilidad, aislando cada consulta en un loop independiente.

***NOTA****: Este es un problema de la librería, no específico del caso de uso.*

En resumen, estos son algunos de los puntos fuertes de LightRAG:

* Respuestas en **20–100 ms** gracias a búsqueda directa sin jerarquías profundas.
* Actualizaciones incrementales **O(m)**, críticas para datos dinámicos (p. ej. añadir publicaciones nuevas en tiempo real).
* La propia librería ofrece una UI incluida y API compatible con *Ollama* para integrar fácilmente LLMs sin depender de proveedores externos.
* Integración con **RAG-Anything** para procesamiento **multimodal** (texto, imágenes, tablas) desde 2025.

Hands-on: Mapeo de 17 Grupos de Investigación UAB
=================================================

* **17 grupos de investigación** en 7 departamentos de la Escuela de Ingeniería de la Universidad Autónoma de Barcelona (UAB).
* **5 *clusters* temáticos principales**:
1. Digital Technologies & Communications (35%)
2. Security & Information Protection (20%)
3. Environmental & Biotechnology (20%)
4. Control Systems & Automation (15%)
5. Hardware & Systems Design (10%)
* **Rango temporal de datos**: 1990–2024 (p.e., GENOCOV activo desde 1990).
* **~100 publicaciones** indexadas en total (papers, tesis, proyectos relevantes).

La idea es que el sistema pueda:

1. **Realizar consultas sobre hechos de manera inmediata** (< 100 ms por respuesta): p.e.“¿Qué es SPCOMNAV?”
2. **Análisis estratégicos profundos**: p. ej. “Oportunidades de colaboración interdepartamental”.
3. **Actualización incremental** al añadir nuevas publicaciones (sin reconstruir todo desde cero).
4. **Escalabilidad**: capacidad para manejar 1,000–10,000 consultas/mes sin degradar rendimiento.
5. **Costo controlado**: infraestructura + API LLM.

1. Arquitectura con Router GPT-5-nano
-------------------------------------

```
┌─────────────────────────────────────────┐  
│            Usuario: Query               │  
└─────────────────────────────────────────┘  
                    │  
                    ▼  
┌─────────────────────────────────────────┐  
│    GPT-5-nano Router (Adaptive RAG)     │  
│   ($0.000023/decisión, 2–3 s)           │  
│   reasoning.effort: "minimal"           │  
└─────────────────────────────────────────┘  
         │                    │  
         ▼                    ▼  
    [80% casos]          [20% casos]  
┌──────────────┐    ┌──────────────────┐  
│   LightRAG   │    │     GraphRAG     │  
│  (Hybrid RAG)│    │    (Graph RAG)   │  
│   (0.02–2 s) │    │     (30–40 s)    │  
└──────────────┘    └──────────────────┘
```
* **Nivel superior**: *Adaptive RAG* — un router inteligente (utilizando el nuevo modelo GPT-5-nano) que clasifica cada pregunta y selecciona el método adecuado.
* **Nivel inferior (izq.)**: LightRAG = Hybrid RAG (fusiona 3 métodos de recuperación en paralelo). Atiende ~80% de casos.
* **Nivel inferior (der.)**: GraphRAG = Graph RAG (navegación jerárquica con grafo). Atiende ~20% de casos.

2. Router Inteligente con GPT-5-nano
====================================

**¿Por qué GPT-5-nano?** OpenAI presentó GPT-5 en julio de 2025 y presentó este modelo específicamente para tareas masivas de enrutamiento/clasificación: costo $0.05 por 1M tokens (20× más barato que GPT-4o), con capacidad de respuesta rápida. Perfecto para decidir, por cada consulta, si usar LightRAG o GraphRAG.

```
from openai import OpenAI  
  
class IntelligentRouter:  
    """  
    Router que usa GPT-5-nano para clasificación ultrarrápida de consultas.  
    Emplea la nueva feature de 'minimal reasoning' para acelerar respuestas.  
    """  
  
    def __init__(self):  
        self.client = OpenAI()  
        self.model = "gpt-5-nano"  
        self.routing_prompt = """  
        Classify this query for RAG system routing:  
          
        Categories:  
        - 'lightrag': Specific facts, entities, quick lookups  
        - 'graphrag': Global analysis, patterns, themes, relationships  
          
        Query: {query}  
          
        Respond with ONLY the category name.  
        """  
      
    async def route_query(self, query: str) -> dict:  
        """Usa GPT-5-nano (razonamiento mínimo) para determinar ruta óptima."""  
        response = await self.client.responses.create(  
            model=self.model,  
            input=self.routing_prompt.format(query=query),  
            reasoning={"effort": "minimal"},   # minimiza pasos de pensamiento  
            text={"verbosity": "low"}          # respuesta concisa (una palabra)  
        )  
        decision = response.output_text.strip().lower()  
        return {  
            "route": decision,  # 'lightrag' o 'graphrag'  
            "confidence": self._calculate_confidence(query, decision),  
            "cost": 0.000023,  # Costo real estimado por decisión (23e-6 USD)  
            "reasoning": "GPT-5-nano classification",  
            "complexity": "low" if decision == "lightrag" else "high"  
        }
```

3. Sistema Adaptive RAG Completo
================================

Finalmente, integramos todo en la clase principal del sistema:

```
class AdaptiveRAGSystem:  
    """  
    Sistema Adaptive RAG que selecciona dinámicamente entre   
    GraphRAG y LightRAG según la complejidad de cada query.  
    """  
    def __init__(self):  
        self.router = IntelligentRouter()  
        self.lightrag = RobustLightRAGWrapper("./lightrag_index") # wrapper que soluciona el problema del Event Loop  
        self.graphrag = GraphRAGWrapper("./graphrag_project")       
        self.metrics = {"total_queries": 0, "lightrag": 0, "graphrag": 0}  
      
    async def query(self, user_query: str) -> dict:  
        """Procesa una query utilizando el router para elegir la vía óptima."""  
          
        start_time = time.time()  
        # 1. Decisión de routing  
        routing = await self.router.route_query(user_query)  
        routing_time = time.time() - start_time  
          
        # 2. Ejecuta la query en el sistema elegido  
        if routing["route"] == "lightrag":  
            answer_text = self.lightrag.query(user_query, mode="hybrid")  
            self.metrics["lightrag"] += 1  
        else:  
            answer_text = self.graphrag.query(user_query, method="global")  
            self.metrics["graphrag"] += 1  
          
        execution_time = time.time() - start_time - routing_time  
        self.metrics["total_queries"] += 1  
        return {  
            "query": user_query,  
            "answer": answer_text,  
            "routing": routing,  
            "times": {  
                "routing": f"{routing_time:.2f}s",  
                "execution": f"{execution_time:.2f}s",  
                "total": f"{time.time() - start_time:.2f}s"  
            },  
            "cost": routing["cost"] + self._calculate_query_cost(routing["route"])  
        }
```
*(En nuestro caso,* `GraphRAGWrapper` *es una abstracción similar a LightRAGWrapper para encapsular llamadas síncronas a GraphRAG.)*

Algunas métricas del sistema en producción:

Press enter or click to view image in full size<img src='https://miro.medium.com/v2/resize:fit:1400/1*pufTpVgRD0Nkg4GvKDC7bA.png' alt='' title='' width='700' height='268' />

***Observaciones:** Para consultas factuales concretas, el router suele responder en ~1–3 s y LightRAG entrega la respuesta casi instantáneamente, manteniendo el total ~1–5 s. Para consultas estratégicas/globales, el router aún responde rápido (2–3 s) pero GraphRAG requiere ~30–40 s para el análisis profundo, llevando el total a ~35–45 s. En todos los casos el router añade una sobrecarga mínima comparado con el tiempo total.*

La gran mayoría de consultas diarias son básicas, y ahí es donde LightRAG destaca por su rapidez. Otras consultas de alto nivel son de tipo estratégicas, donde GraphRAG aporta valor pese a una latencia mayor. La ventaja de estas arquitecturas dinámicas con un sistema híbrido por debajo es evitar gastar +30 segundos en el 80% de preguntas que no lo requieren, sin dejar de cubrir el 20% de preguntas complejas con sistemas que dan vuenos resultados.

Esta es una estimación de costes con un escalado para 1000 y 10.000 consultas diarias:

Press enter or click to view image in full size<img src='https://miro.medium.com/v2/resize:fit:1400/1*Tdt0F80sIa0RsPY76wGHkw.png' alt='' title='' width='700' height='146' />

***Observaciones:** *Estimado asumiendo ~80% consultas van a LightRAG (ejecutadas en local o con modelo menor, costo marginal) y ~20% a GraphRAG (ejecutado con GPT-4o o similar) + costo del router GPT-5-nano por decisión.**

Incluso con 10k consultas al mes (~330 diarias), el costo total se mantuvo alrededor de $30 USD. El router GPT-5-nano aporta una fracción mínima del costo (<1%), y las consultas GraphRAG (20%) dominan el gasto. Aun así, comparar $30 con una alternativa de usar siempre GPT-4/GraphRAG para todo (que habría sido mucho más costosa) evidencia el ahorro significativo del enfoque adaptativo.

Algunos ejemplos de preguntas reales:

**Query LightRAG, ~0.02 s**

Q: *“Which research group specializes in circular economy?”*

A: **GENOCOV** (Group of biological treatment of liquid and gaseous effluents) *Especialización:* Economía circular a través de:

* Procesos biológicos de tratamiento de aguas residuales.
* Recuperación de recursos a partir de corrientes de desecho.
* Ingeniería ambiental sostenible.

**Query GraphRAG, ~39 s**

Q: *“What are the main collaboration opportunities between departments?”*

A: *El análisis identifica 5 grandes oportunidades interdisciplinarias:*

**1. AI-Biomedical Convergence**

* **Departamentos involucrados:** Information & Communications + Chemical/Biological.
* **Grupos clave:** WIN, CSCG + GENOCOV, GECT.

AI aplicada a descubrimiento de fármacos, medicina personalizada.

**2. Smart Cities & IoT Platforms**

* **Departamentos:** Telecommunications + Computer Architecture + Electronic Engineering.
* **Grupos clave:** SPCOMNAV, ASAC + HPC4EAS + DCSI.

Sistemas urbanos inteligentes, optimización de tráfico, gestión energética.

**3. Quantum Technologies Initiative**

* **Departamentos:** Information & Communications + Telecommunications.
* **Grupos clave:** Q-CSI + SPCOMNAV.

Redes cuánticas, comunicaciones seguras de próxima generación.

**4. Sustainable Tech Framework**

* **Iniciativa transversal (varios departamentos)**.
* **Grupos clave:** GENOCOV + GECT + equipos de *smart grids*.

Economía circular, integración de energías renovables, tecnología verde.

**5. Security & Privacy Platform**

**Departamentos:** Information & Communications + (colaboración amplia con otros).

* **Grupos clave:** CSCG + equipos de seguridad de redes.

Ciberseguridad para IoT, aplicaciones de blockchain, privacidad de datos.

Conclusiones
============

La experiencia en la UAB demuestra que no existe un ganador único en la batalla **GraphRAG vs LightRAG**. La clave está en combinarlos bajo un enfoque **Adaptive RAG**, donde un router inteligente basado en **GPT-5-nano** decide en tiempo real qué arquitectura aplicar en cada consulta. Este equilibrio aporta rapidez en el 80% de los casos y profundidad analítica en el 20% restante, con un coste controlado y sin sacrificar fiabilidad.

La lección principal es clara: en producción no basta con elegir una librería de moda, sino diseñar sistemas capaces de adaptarse dinámicamente a las necesidades de cada usuario, cada query y sobretodo el caso de uso específico. El impacto práctico es evidente: ahorro de costes, reducción de latencias y escalabilidad real sin comprometer la calidad de las respuestas.

What’s next
===========

Quedan aún retos por explorar antes de consolidar estos sistemas como estándar. Algunos caminos inmediatos:

* **Integración multimodal**: extender el Adaptive RAG a consultas que combinen texto, imágenes y datos tabulares.
* **Agentes sobre RAG**: conectar este router con frameworks como LangGraph para orquestar flujos más complejos, incorporando planificación y memoria a largo plazo.
* **Optimización de coste y latencia**: experimentar con versiones aún más ligeras de los modelos clasificadores, o incluso modelos especializados entrenados in-house para tareas de routing.
* **Aplicaciones verticales**: replicar esta arquitectura en otros sectores más allá de la investigación universitaria: finanzas, salud, administración pública.

En definitiva, **el ecosistema RAG en 2025 es más un sistema vivo que un conjunto de librerías aisladas**. La invitación queda abierta: explorar, probar y compartir nuevas combinaciones que lleven la tecnología un paso más allá de lo que hoy entendemos por técnicas de recuperación aumentada o RAG. Puedes leer otros artículos publicados hace un tiempo aquí:

* [**Comparativa Naive RAG vs ReAct Agent utilizando LlamaIndex**](/@jddam/comparativa-naive-rag-vs-react-agent-utilizando-llamaindex-24fb11577574)

**Comparte tu experiencia:**

Estoy abierto a colaborar y discutir sobre las posibilidades que ofrece la inteligencia artificial y cómo trabajar juntos para explorar y construir soluciones en diferentes sectores. Si tienes ideas, preguntas o simplemente quieres hablar de ello, escríbeme:

* GitHub: <https://github.com/albertgilopez>
* LinkedIn: <https://www.linkedin.com/in/albertgilopez/>
* M.IA, tu asistente financiero inteligente: <https://himia.app/>
* Inteligencia Artificial Generativa en español: <https://www.codigollm.es/>

