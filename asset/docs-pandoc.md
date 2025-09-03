::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {.page-body .full-width .flush .docs-page}
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {.docs-markdown-page .docs-markdown-content .markdown-prompt-blockquote}
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {.flex .w-full .items-start}
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: docs-markdown-page-inner
<div>

::::::: {.title-container .flex .flex-col .items-baseline .justify-between .lg:flex-row}
:::: {.order-2 .lg:order-1}
# Text generation {#page-top .docs-markdown-page-title}

::: docs-markdown-page-subtitle
Learn how to prompt a model to generate text.
:::
::::

:::: {.order-1 .-mt-2.5 .mb-4 .flex .w-full .flex-row .items-end .justify-between .gap-2 .lg:order-2 .lg:mt-0 .lg:mb-0 .lg:ml-4 .lg:w-auto .lg:flex-col .lg:justify-start .lg:px-1}
::: {.-order-1 .-ml-1.5 .lg:ml-0}
[[[![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjFlbSIgaGVpZ2h0PSIxZW0iPjxwYXRoIGQ9Ik0xMi43NTg3IDJIMTYuMjQxM0MxNy4wNDYzIDEuOTk5OTkgMTcuNzEwNiAxLjk5OTk4IDE4LjI1MTggMi4wNDQxOUMxOC44MTM5IDIuMDkwMTIgMTkuMzMwNiAyLjE4ODY4IDE5LjgxNiAyLjQzNTk3QzIwLjU2ODYgMi44MTk0NyAyMS4xODA1IDMuNDMxMzkgMjEuNTY0IDQuMTg0MDRDMjEuODExMyA0LjY2OTM3IDIxLjkwOTkgNS4xODYwOCAyMS45NTU4IDUuNzQ4MTdDMjIgNi4yODkzNiAyMiA2Ljk1MzcyIDIyIDcuNzU4NjhWMTEuMjQxM0MyMiAxMi4wNDYzIDIyIDEyLjcxMDYgMjEuOTU1OCAxMy4yNTE4QzIxLjkwOTkgMTMuODEzOSAyMS44MTEzIDE0LjMzMDYgMjEuNTY0IDE0LjgxNkMyMS4xODA1IDE1LjU2ODYgMjAuNTY4NiAxNi4xODA1IDE5LjgxNiAxNi41NjRDMTkuMzMwNiAxNi44MTEzIDE4LjgxMzkgMTYuOTA5OSAxOC4yNTE4IDE2Ljk1NThDMTcuODkwNiAxNi45ODUzIDE3LjQ3NDUgMTYuOTk1MSAxNi45OTg0IDE2Ljk5ODRDMTYuOTk1MSAxNy40NzQ1IDE2Ljk4NTMgMTcuODkwNiAxNi45NTU4IDE4LjI1MThDMTYuOTA5OSAxOC44MTM5IDE2LjgxMTMgMTkuMzMwNiAxNi41NjQgMTkuODE2QzE2LjE4MDUgMjAuNTY4NiAxNS41Njg2IDIxLjE4MDUgMTQuODE2IDIxLjU2NEMxNC4zMzA2IDIxLjgxMTMgMTMuODEzOSAyMS45MDk5IDEzLjI1MTggMjEuOTU1OEMxMi43MTA2IDIyIDEyLjA0NjMgMjIgMTEuMjQxMyAyMkg3Ljc1ODY4QzYuOTUzNzIgMjIgNi4yODkzNiAyMiA1Ljc0ODE4IDIxLjk1NThDNS4xODYwOCAyMS45MDk5IDQuNjY5MzcgMjEuODExMyA0LjE4NDA0IDIxLjU2NEMzLjQzMTM5IDIxLjE4MDUgMi44MTk0NyAyMC41Njg2IDIuNDM1OTcgMTkuODE2QzIuMTg4NjggMTkuMzMwNiAyLjA5MDEyIDE4LjgxMzkgMi4wNDQxOSAxOC4yNTE4QzEuOTk5OTggMTcuNzEwNiAxLjk5OTk5IDE3LjA0NjMgMiAxNi4yNDEzVjEyLjc1ODdDMS45OTk5OSAxMS45NTM3IDEuOTk5OTggMTEuMjg5NCAyLjA0NDE5IDEwLjc0ODJDMi4wOTAxMiAxMC4xODYxIDIuMTg4NjggOS42NjkzNyAyLjQzNTk3IDkuMTg0MDRDMi44MTk0NyA4LjQzMTM5IDMuNDMxMzkgNy44MTk0NyA0LjE4NDA0IDcuNDM1OThDNC42NjkzNyA3LjE4ODY4IDUuMTg2MDggNy4wOTAxMiA1Ljc0ODE3IDcuMDQ0MTlDNi4xMDkzOSA3LjAxNDY4IDYuNTI1NDggNy4wMDQ4NyA3LjAwMTYyIDcuMDAxNjJDNy4wMDQ4NyA2LjUyNTQ4IDcuMDE0NjggNi4xMDkzOSA3LjA0NDE5IDUuNzQ4MTdDNy4wOTAxMiA1LjE4NjA4IDcuMTg4NjggNC42NjkzNyA3LjQzNTk4IDQuMTg0MDRDNy44MTk0NyAzLjQzMTM5IDguNDMxMzkgMi44MTk0NyA5LjE4NDA0IDIuNDM1OTdDOS42NjkzNyAyLjE4ODY4IDEwLjE4NjEgMi4wOTAxMiAxMC43NDgyIDIuMDQ0MTlDMTEuMjg5NCAxLjk5OTk4IDExLjk1MzcgMS45OTk5OSAxMi43NTg3IDJaTTkuMDAxNzYgN0wxMS4yNDEzIDdDMTIuMDQ2MyA2Ljk5OTk5IDEyLjcxMDYgNi45OTk5OCAxMy4yNTE4IDcuMDQ0MTlDMTMuODEzOSA3LjA5MDEyIDE0LjMzMDYgNy4xODg2OCAxNC44MTYgNy40MzU5OEMxNS41Njg2IDcuODE5NDcgMTYuMTgwNSA4LjQzMTM5IDE2LjU2NCA5LjE4NDA0QzE2LjgxMTMgOS42NjkzNyAxNi45MDk5IDEwLjE4NjEgMTYuOTU1OCAxMC43NDgyQzE3IDExLjI4OTQgMTcgMTEuOTUzNyAxNyAxMi43NTg3VjE0Ljk5ODJDMTcuNDQ1NSAxNC45OTUxIDE3Ljc5NTQgMTQuOTg2NCAxOC4wODkgMTQuOTYyNEMxOC41Mjc0IDE0LjkyNjYgMTguNzUxNiAxNC44NjE3IDE4LjkwOCAxNC43ODJDMTkuMjg0MyAxNC41OTAzIDE5LjU5MDMgMTQuMjg0MyAxOS43ODIgMTMuOTA4QzE5Ljg2MTcgMTMuNzUxNiAxOS45MjY2IDEzLjUyNzQgMTkuOTYyNCAxMy4wODlDMTkuOTk5MiAxMi42Mzg5IDIwIDEyLjA1NjYgMjAgMTEuMlY3LjhDMjAgNi45NDM0MiAxOS45OTkyIDYuMzYxMTMgMTkuOTYyNCA1LjkxMTA0QzE5LjkyNjYgNS40NzI2MiAxOS44NjE3IDUuMjQ4NDIgMTkuNzgyIDUuMDkyMDJDMTkuNTkwMyA0LjcxNTcgMTkuMjg0MyA0LjQwOTczIDE4LjkwOCA0LjIxNzk5QzE4Ljc1MTYgNC4xMzgzIDE4LjUyNzQgNC4wNzMzNyAxOC4wODkgNC4wMzc1NUMxNy42Mzg5IDQuMDAwNzggMTcuMDU2NiA0IDE2LjIgNEgxMi44QzExLjk0MzQgNCAxMS4zNjExIDQuMDAwNzggMTAuOTExIDQuMDM3NTVDMTAuNDcyNiA0LjA3MzM3IDEwLjI0ODQgNC4xMzgzIDEwLjA5MiA0LjIxNzk5QzkuNzE1NyA0LjQwOTczIDkuNDA5NzMgNC43MTU3IDkuMjE3OTkgNS4wOTIwMkM5LjEzODMgNS4yNDg0MiA5LjA3MzM3IDUuNDcyNjIgOS4wMzc1NSA1LjkxMTA0QzkuMDEzNTcgNi4yMDQ2MyA5LjAwNDg5IDYuNTU0NDcgOS4wMDE3NiA3Wk01LjkxMTA0IDkuMDM3NTVDNS40NzI2MiA5LjA3MzM3IDUuMjQ4NDIgOS4xMzgzIDUuMDkyMDIgOS4yMTc5OUM0LjcxNTcgOS40MDk3MyA0LjQwOTczIDkuNzE1NyA0LjIxNzk5IDEwLjA5MkM0LjEzODMgMTAuMjQ4NCA0LjA3MzM3IDEwLjQ3MjYgNC4wMzc1NSAxMC45MTFDNC4wMDA3OCAxMS4zNjExIDQgMTEuOTQzNCA0IDEyLjhWMTYuMkM0IDE3LjA1NjYgNC4wMDA3OCAxNy42Mzg5IDQuMDM3NTUgMTguMDg5QzQuMDczMzcgMTguNTI3NCA0LjEzODMgMTguNzUxNiA0LjIxNzk5IDE4LjkwOEM0LjQwOTczIDE5LjI4NDMgNC43MTU3IDE5LjU5MDMgNS4wOTIwMiAxOS43ODJDNS4yNDg0MiAxOS44NjE3IDUuNDcyNjIgMTkuOTI2NiA1LjkxMTA0IDE5Ljk2MjRDNi4zNjExMyAxOS45OTkyIDYuOTQzNDIgMjAgNy44IDIwSDExLjJDMTIuMDU2NiAyMCAxMi42Mzg5IDE5Ljk5OTIgMTMuMDg5IDE5Ljk2MjRDMTMuNTI3NCAxOS45MjY2IDEzLjc1MTYgMTkuODYxNyAxMy45MDggMTkuNzgyQzE0LjI4NDMgMTkuNTkwMyAxNC41OTAzIDE5LjI4NDMgMTQuNzgyIDE4LjkwOEMxNC44NjE3IDE4Ljc1MTYgMTQuOTI2NiAxOC41Mjc0IDE0Ljk2MjQgMTguMDg5QzE0Ljk5OTIgMTcuNjM4OSAxNSAxNy4wNTY2IDE1IDE2LjJWMTIuOEMxNSAxMS45NDM0IDE0Ljk5OTIgMTEuMzYxMSAxNC45NjI0IDEwLjkxMUMxNC45MjY2IDEwLjQ3MjYgMTQuODYxNyAxMC4yNDg0IDE0Ljc4MiAxMC4wOTJDMTQuNTkwMyA5LjcxNTcgMTQuMjg0MyA5LjQwOTczIDEzLjkwOCA5LjIxNzk5QzEzLjc1MTYgOS4xMzgzIDEzLjUyNzQgOS4wNzMzNyAxMy4wODkgOS4wMzc1NUMxMi42Mzg5IDkuMDAwNzggMTIuMDU2NiA5IDExLjIgOUg3LjhDNi45NDM0MiA5IDYuMzYxMTMgOS4wMDA3OCA1LjkxMTA0IDkuMDM3NTVaIiAvPjwvc3ZnPg==)]{._4jUWi
.pdMy8}]{.block .relative .w-[var(--button-icon-size)]
.h-[var(--button-icon-size)] transition-position="absolute"
style="--tg-will-change: transform, opacity; --tg-enter-opacity: 1; --tg-enter-transform: scale(1); --tg-enter-filter: none; --tg-enter-duration: 300ms; --tg-enter-delay: 150ms; --tg-enter-timing-function: var(--cubic-enter); --tg-exit-opacity: 0; --tg-exit-transform: scale(0.6); --tg-exit-filter: none; --tg-exit-duration: 150ms; --tg-exit-delay: 0ms; --tg-exit-timing-function: var(--cubic-exit); --tg-initial-opacity: 0; --tg-initial-transform: scale(0.6); --tg-initial-filter: none;"}Copy
page]{.NBPKZ}
:::
::::
:::::::

With the OpenAI API, you can use a [large language
model](/docs/models){.kZ98Q underline=""} to generate text from a
prompt, as you might using [ChatGPT](https://chatgpt.com){.kZ98Q
target="_blank" rel="noopener noreferrer" underline=""}. Models can
generate almost any kind of text response---like code, mathematical
equations, structured JSON data, or human-like prose.

Here\'s a simple example using the [Responses
API](/docs/api-reference/responses){.kZ98Q underline=""}.

::::::::::: {.code-sample .dark-mode}
:::::: code-sample-header
::: {.code-sample-title .body-small}
Generate text from a simple prompt
:::

:::: exclude-from-copy
[[python]{.ktL9G}]{#select-trigger-:ru: .fsluc role="button"
tabindex="0" variant="ghost" data-size="sm" data-selected="true"
aria-disabled="false" type="button" aria-haspopup="dialog"
aria-expanded="false" aria-controls="radix-:r10:" state="closed"}

::: FJZOe
![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMWVtIiBoZWlnaHQ9IjFlbSIgdmlld2JveD0iMCAwIDEwIDE2IiBmaWxsPSJjdXJyZW50Q29sb3IiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgY2xhc3M9InlnenM2Ij48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTQuMzQxNTEgMC43NDc0MjNDNC43MTg1NCAwLjQxNzUyNiA1LjI4MTQ5IDAuNDE3NTI2IDUuNjU4NTIgMC43NDc0MjNMOS42NTg1MiA0LjI0NzQyQzEwLjA3NDIgNC42MTExMSAxMC4xMTYzIDUuMjQyODcgOS43NTI1OSA1LjY1ODVDOS4zODg5MSA2LjA3NDE0IDguNzU3MTUgNi4xMTYyNiA4LjM0MTUxIDUuNzUyNThMNS4wMDAwMSAyLjgyODc3TDEuNjU4NTIgNS43NTI1OEMxLjI0Mjg4IDYuMTE2MjYgMC42MTExMiA2LjA3NDE0IDAuMjQ3NDM4IDUuNjU4NUMtMC4xMTYyNDQgNS4yNDI4NyAtMC4wNzQxMjY3IDQuNjExMTEgMC4zNDE1MSA0LjI0NzQyTDQuMzQxNTEgMC43NDc0MjNaTTAuMjQ2MDY1IDEwLjM1NzhDMC42MDg4NzkgOS45NDEzOSAxLjI0MDU1IDkuODk3OTUgMS42NTY5NSAxMC4yNjA4TDUuMDAwMDEgMTMuMTczN0w4LjM0MzA4IDEwLjI2MDhDOC43NTk0OCA5Ljg5Nzk1IDkuMzkxMTUgOS45NDEzOSA5Ljc1Mzk2IDEwLjM1NzhDMTAuMTE2OCAxMC43NzQyIDEwLjA3MzMgMTEuNDA1OCA5LjY1Njk1IDExLjc2ODdMNS42NTY5NSAxNS4yNTM5QzUuMjgwNDMgMTUuNTgyIDQuNzE5NiAxNS41ODIgNC4zNDMwOCAxNS4yNTM5TDAuMzQzMDgyIDExLjc2ODdDLTAuMDczMzEyOCAxMS40MDU4IC0wLjExNjc0OSAxMC43NzQyIDAuMjQ2MDY1IDEwLjM1NzhaIiAvPjwvc3ZnPg==){.ygzs6}
:::
::::

[[[![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjFlbSIgaGVpZ2h0PSIxZW0iPjxwYXRoIGQ9Ik0xMi43NTg3IDJIMTYuMjQxM0MxNy4wNDYzIDEuOTk5OTkgMTcuNzEwNiAxLjk5OTk4IDE4LjI1MTggMi4wNDQxOUMxOC44MTM5IDIuMDkwMTIgMTkuMzMwNiAyLjE4ODY4IDE5LjgxNiAyLjQzNTk3QzIwLjU2ODYgMi44MTk0NyAyMS4xODA1IDMuNDMxMzkgMjEuNTY0IDQuMTg0MDRDMjEuODExMyA0LjY2OTM3IDIxLjkwOTkgNS4xODYwOCAyMS45NTU4IDUuNzQ4MTdDMjIgNi4yODkzNiAyMiA2Ljk1MzcyIDIyIDcuNzU4NjhWMTEuMjQxM0MyMiAxMi4wNDYzIDIyIDEyLjcxMDYgMjEuOTU1OCAxMy4yNTE4QzIxLjkwOTkgMTMuODEzOSAyMS44MTEzIDE0LjMzMDYgMjEuNTY0IDE0LjgxNkMyMS4xODA1IDE1LjU2ODYgMjAuNTY4NiAxNi4xODA1IDE5LjgxNiAxNi41NjRDMTkuMzMwNiAxNi44MTEzIDE4LjgxMzkgMTYuOTA5OSAxOC4yNTE4IDE2Ljk1NThDMTcuODkwNiAxNi45ODUzIDE3LjQ3NDUgMTYuOTk1MSAxNi45OTg0IDE2Ljk5ODRDMTYuOTk1MSAxNy40NzQ1IDE2Ljk4NTMgMTcuODkwNiAxNi45NTU4IDE4LjI1MThDMTYuOTA5OSAxOC44MTM5IDE2LjgxMTMgMTkuMzMwNiAxNi41NjQgMTkuODE2QzE2LjE4MDUgMjAuNTY4NiAxNS41Njg2IDIxLjE4MDUgMTQuODE2IDIxLjU2NEMxNC4zMzA2IDIxLjgxMTMgMTMuODEzOSAyMS45MDk5IDEzLjI1MTggMjEuOTU1OEMxMi43MTA2IDIyIDEyLjA0NjMgMjIgMTEuMjQxMyAyMkg3Ljc1ODY4QzYuOTUzNzIgMjIgNi4yODkzNiAyMiA1Ljc0ODE4IDIxLjk1NThDNS4xODYwOCAyMS45MDk5IDQuNjY5MzcgMjEuODExMyA0LjE4NDA0IDIxLjU2NEMzLjQzMTM5IDIxLjE4MDUgMi44MTk0NyAyMC41Njg2IDIuNDM1OTcgMTkuODE2QzIuMTg4NjggMTkuMzMwNiAyLjA5MDEyIDE4LjgxMzkgMi4wNDQxOSAxOC4yNTE4QzEuOTk5OTggMTcuNzEwNiAxLjk5OTk5IDE3LjA0NjMgMiAxNi4yNDEzVjEyLjc1ODdDMS45OTk5OSAxMS45NTM3IDEuOTk5OTggMTEuMjg5NCAyLjA0NDE5IDEwLjc0ODJDMi4wOTAxMiAxMC4xODYxIDIuMTg4NjggOS42NjkzNyAyLjQzNTk3IDkuMTg0MDRDMi44MTk0NyA4LjQzMTM5IDMuNDMxMzkgNy44MTk0NyA0LjE4NDA0IDcuNDM1OThDNC42NjkzNyA3LjE4ODY4IDUuMTg2MDggNy4wOTAxMiA1Ljc0ODE3IDcuMDQ0MTlDNi4xMDkzOSA3LjAxNDY4IDYuNTI1NDggNy4wMDQ4NyA3LjAwMTYyIDcuMDAxNjJDNy4wMDQ4NyA2LjUyNTQ4IDcuMDE0NjggNi4xMDkzOSA3LjA0NDE5IDUuNzQ4MTdDNy4wOTAxMiA1LjE4NjA4IDcuMTg4NjggNC42NjkzNyA3LjQzNTk4IDQuMTg0MDRDNy44MTk0NyAzLjQzMTM5IDguNDMxMzkgMi44MTk0NyA5LjE4NDA0IDIuNDM1OTdDOS42NjkzNyAyLjE4ODY4IDEwLjE4NjEgMi4wOTAxMiAxMC43NDgyIDIuMDQ0MTlDMTEuMjg5NCAxLjk5OTk4IDExLjk1MzcgMS45OTk5OSAxMi43NTg3IDJaTTkuMDAxNzYgN0wxMS4yNDEzIDdDMTIuMDQ2MyA2Ljk5OTk5IDEyLjcxMDYgNi45OTk5OCAxMy4yNTE4IDcuMDQ0MTlDMTMuODEzOSA3LjA5MDEyIDE0LjMzMDYgNy4xODg2OCAxNC44MTYgNy40MzU5OEMxNS41Njg2IDcuODE5NDcgMTYuMTgwNSA4LjQzMTM5IDE2LjU2NCA5LjE4NDA0QzE2LjgxMTMgOS42NjkzNyAxNi45MDk5IDEwLjE4NjEgMTYuOTU1OCAxMC43NDgyQzE3IDExLjI4OTQgMTcgMTEuOTUzNyAxNyAxMi43NTg3VjE0Ljk5ODJDMTcuNDQ1NSAxNC45OTUxIDE3Ljc5NTQgMTQuOTg2NCAxOC4wODkgMTQuOTYyNEMxOC41Mjc0IDE0LjkyNjYgMTguNzUxNiAxNC44NjE3IDE4LjkwOCAxNC43ODJDMTkuMjg0MyAxNC41OTAzIDE5LjU5MDMgMTQuMjg0MyAxOS43ODIgMTMuOTA4QzE5Ljg2MTcgMTMuNzUxNiAxOS45MjY2IDEzLjUyNzQgMTkuOTYyNCAxMy4wODlDMTkuOTk5MiAxMi42Mzg5IDIwIDEyLjA1NjYgMjAgMTEuMlY3LjhDMjAgNi45NDM0MiAxOS45OTkyIDYuMzYxMTMgMTkuOTYyNCA1LjkxMTA0QzE5LjkyNjYgNS40NzI2MiAxOS44NjE3IDUuMjQ4NDIgMTkuNzgyIDUuMDkyMDJDMTkuNTkwMyA0LjcxNTcgMTkuMjg0MyA0LjQwOTczIDE4LjkwOCA0LjIxNzk5QzE4Ljc1MTYgNC4xMzgzIDE4LjUyNzQgNC4wNzMzNyAxOC4wODkgNC4wMzc1NUMxNy42Mzg5IDQuMDAwNzggMTcuMDU2NiA0IDE2LjIgNEgxMi44QzExLjk0MzQgNCAxMS4zNjExIDQuMDAwNzggMTAuOTExIDQuMDM3NTVDMTAuNDcyNiA0LjA3MzM3IDEwLjI0ODQgNC4xMzgzIDEwLjA5MiA0LjIxNzk5QzkuNzE1NyA0LjQwOTczIDkuNDA5NzMgNC43MTU3IDkuMjE3OTkgNS4wOTIwMkM5LjEzODMgNS4yNDg0MiA5LjA3MzM3IDUuNDcyNjIgOS4wMzc1NSA1LjkxMTA0QzkuMDEzNTcgNi4yMDQ2MyA5LjAwNDg5IDYuNTU0NDcgOS4wMDE3NiA3Wk01LjkxMTA0IDkuMDM3NTVDNS40NzI2MiA5LjA3MzM3IDUuMjQ4NDIgOS4xMzgzIDUuMDkyMDIgOS4yMTc5OUM0LjcxNTcgOS40MDk3MyA0LjQwOTczIDkuNzE1NyA0LjIxNzk5IDEwLjA5MkM0LjEzODMgMTAuMjQ4NCA0LjA3MzM3IDEwLjQ3MjYgNC4wMzc1NSAxMC45MTFDNC4wMDA3OCAxMS4zNjExIDQgMTEuOTQzNCA0IDEyLjhWMTYuMkM0IDE3LjA1NjYgNC4wMDA3OCAxNy42Mzg5IDQuMDM3NTUgMTguMDg5QzQuMDczMzcgMTguNTI3NCA0LjEzODMgMTguNzUxNiA0LjIxNzk5IDE4LjkwOEM0LjQwOTczIDE5LjI4NDMgNC43MTU3IDE5LjU5MDMgNS4wOTIwMiAxOS43ODJDNS4yNDg0MiAxOS44NjE3IDUuNDcyNjIgMTkuOTI2NiA1LjkxMTA0IDE5Ljk2MjRDNi4zNjExMyAxOS45OTkyIDYuOTQzNDIgMjAgNy44IDIwSDExLjJDMTIuMDU2NiAyMCAxMi42Mzg5IDE5Ljk5OTIgMTMuMDg5IDE5Ljk2MjRDMTMuNTI3NCAxOS45MjY2IDEzLjc1MTYgMTkuODYxNyAxMy45MDggMTkuNzgyQzE0LjI4NDMgMTkuNTkwMyAxNC41OTAzIDE5LjI4NDMgMTQuNzgyIDE4LjkwOEMxNC44NjE3IDE4Ljc1MTYgMTQuOTI2NiAxOC41Mjc0IDE0Ljk2MjQgMTguMDg5QzE0Ljk5OTIgMTcuNjM4OSAxNSAxNy4wNTY2IDE1IDE2LjJWMTIuOEMxNSAxMS45NDM0IDE0Ljk5OTIgMTEuMzYxMSAxNC45NjI0IDEwLjkxMUMxNC45MjY2IDEwLjQ3MjYgMTQuODYxNyAxMC4yNDg0IDE0Ljc4MiAxMC4wOTJDMTQuNTkwMyA5LjcxNTcgMTQuMjg0MyA5LjQwOTczIDEzLjkwOCA5LjIxNzk5QzEzLjc1MTYgOS4xMzgzIDEzLjUyNzQgOS4wNzMzNyAxMy4wODkgOS4wMzc1NUMxMi42Mzg5IDkuMDAwNzggMTIuMDU2NiA5IDExLjIgOUg3LjhDNi45NDM0MiA5IDYuMzYxMTMgOS4wMDA3OCA1LjkxMTA0IDkuMDM3NTVaIiAvPjwvc3ZnPg==)]{._4jUWi
.pdMy8}]{.block .relative .w-[var(--button-icon-size)]
.h-[var(--button-icon-size)] transition-position="absolute"
style="--tg-will-change: transform, opacity; --tg-enter-opacity: 1; --tg-enter-transform: scale(1); --tg-enter-filter: none; --tg-enter-duration: 300ms; --tg-enter-delay: 150ms; --tg-enter-timing-function: var(--cubic-enter); --tg-exit-opacity: 0; --tg-exit-transform: scale(0.6); --tg-exit-filter: none; --tg-exit-duration: 150ms; --tg-exit-delay: 0ms; --tg-exit-timing-function: var(--cubic-exit); --tg-initial-opacity: 0; --tg-initial-transform: scale(0.6); --tg-initial-filter: none;"}]{.NBPKZ}
::::::

:::::: {.code-sample-body .code-sample-body-small .code-sample-body-with-header}
::: {.code-block .hidden}
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-5",
    input: "Write a one-sentence bedtime story about a unicorn."
});

console.log(response.output_text);
```
:::

::: code-block
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
```
:::

::: {.code-block .hidden}
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-5",
        "input": "Write a one-sentence bedtime story about a unicorn."
    }'
```
:::
::::::
:::::::::::

An array of content generated by the model is in the `output` property
of the response. In this simple example, we have just one output which
looks like this:

::::: {.code-sample .dark-mode}
:::: {.code-sample-body .code-sample-body-large}
::: code-sample-copy-float
[[[![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjFlbSIgaGVpZ2h0PSIxZW0iPjxwYXRoIGQ9Ik0xMi43NTg3IDJIMTYuMjQxM0MxNy4wNDYzIDEuOTk5OTkgMTcuNzEwNiAxLjk5OTk4IDE4LjI1MTggMi4wNDQxOUMxOC44MTM5IDIuMDkwMTIgMTkuMzMwNiAyLjE4ODY4IDE5LjgxNiAyLjQzNTk3QzIwLjU2ODYgMi44MTk0NyAyMS4xODA1IDMuNDMxMzkgMjEuNTY0IDQuMTg0MDRDMjEuODExMyA0LjY2OTM3IDIxLjkwOTkgNS4xODYwOCAyMS45NTU4IDUuNzQ4MTdDMjIgNi4yODkzNiAyMiA2Ljk1MzcyIDIyIDcuNzU4NjhWMTEuMjQxM0MyMiAxMi4wNDYzIDIyIDEyLjcxMDYgMjEuOTU1OCAxMy4yNTE4QzIxLjkwOTkgMTMuODEzOSAyMS44MTEzIDE0LjMzMDYgMjEuNTY0IDE0LjgxNkMyMS4xODA1IDE1LjU2ODYgMjAuNTY4NiAxNi4xODA1IDE5LjgxNiAxNi41NjRDMTkuMzMwNiAxNi44MTEzIDE4LjgxMzkgMTYuOTA5OSAxOC4yNTE4IDE2Ljk1NThDMTcuODkwNiAxNi45ODUzIDE3LjQ3NDUgMTYuOTk1MSAxNi45OTg0IDE2Ljk5ODRDMTYuOTk1MSAxNy40NzQ1IDE2Ljk4NTMgMTcuODkwNiAxNi45NTU4IDE4LjI1MThDMTYuOTA5OSAxOC44MTM5IDE2LjgxMTMgMTkuMzMwNiAxNi41NjQgMTkuODE2QzE2LjE4MDUgMjAuNTY4NiAxNS41Njg2IDIxLjE4MDUgMTQuODE2IDIxLjU2NEMxNC4zMzA2IDIxLjgxMTMgMTMuODEzOSAyMS45MDk5IDEzLjI1MTggMjEuOTU1OEMxMi43MTA2IDIyIDEyLjA0NjMgMjIgMTEuMjQxMyAyMkg3Ljc1ODY4QzYuOTUzNzIgMjIgNi4yODkzNiAyMiA1Ljc0ODE4IDIxLjk1NThDNS4xODYwOCAyMS45MDk5IDQuNjY5MzcgMjEuODExMyA0LjE4NDA0IDIxLjU2NEMzLjQzMTM5IDIxLjE4MDUgMi44MTk0NyAyMC41Njg2IDIuNDM1OTcgMTkuODE2QzIuMTg4NjggMTkuMzMwNiAyLjA5MDEyIDE4LjgxMzkgMi4wNDQxOSAxOC4yNTE4QzEuOTk5OTggMTcuNzEwNiAxLjk5OTk5IDE3LjA0NjMgMiAxNi4yNDEzVjEyLjc1ODdDMS45OTk5OSAxMS45NTM3IDEuOTk5OTggMTEuMjg5NCAyLjA0NDE5IDEwLjc0ODJDMi4wOTAxMiAxMC4xODYxIDIuMTg4NjggOS42NjkzNyAyLjQzNTk3IDkuMTg0MDRDMi44MTk0NyA4LjQzMTM5IDMuNDMxMzkgNy44MTk0NyA0LjE4NDA0IDcuNDM1OThDNC42NjkzNyA3LjE4ODY4IDUuMTg2MDggNy4wOTAxMiA1Ljc0ODE3IDcuMDQ0MTlDNi4xMDkzOSA3LjAxNDY4IDYuNTI1NDggNy4wMDQ4NyA3LjAwMTYyIDcuMDAxNjJDNy4wMDQ4NyA2LjUyNTQ4IDcuMDE0NjggNi4xMDkzOSA3LjA0NDE5IDUuNzQ4MTdDNy4wOTAxMiA1LjE4NjA4IDcuMTg4NjggNC42NjkzNyA3LjQzNTk4IDQuMTg0MDRDNy44MTk0NyAzLjQzMTM5IDguNDMxMzkgMi44MTk0NyA5LjE4NDA0IDIuNDM1OTdDOS42NjkzNyAyLjE4ODY4IDEwLjE4NjEgMi4wOTAxMiAxMC43NDgyIDIuMDQ0MTlDMTEuMjg5NCAxLjk5OTk4IDExLjk1MzcgMS45OTk5OSAxMi43NTg3IDJaTTkuMDAxNzYgN0wxMS4yNDEzIDdDMTIuMDQ2MyA2Ljk5OTk5IDEyLjcxMDYgNi45OTk5OCAxMy4yNTE4IDcuMDQ0MTlDMTMuODEzOSA3LjA5MDEyIDE0LjMzMDYgNy4xODg2OCAxNC44MTYgNy40MzU5OEMxNS41Njg2IDcuODE5NDcgMTYuMTgwNSA4LjQzMTM5IDE2LjU2NCA5LjE4NDA0QzE2LjgxMTMgOS42NjkzNyAxNi45MDk5IDEwLjE4NjEgMTYuOTU1OCAxMC43NDgyQzE3IDExLjI4OTQgMTcgMTEuOTUzNyAxNyAxMi43NTg3VjE0Ljk5ODJDMTcuNDQ1NSAxNC45OTUxIDE3Ljc5NTQgMTQuOTg2NCAxOC4wODkgMTQuOTYyNEMxOC41Mjc0IDE0LjkyNjYgMTguNzUxNiAxNC44NjE3IDE4LjkwOCAxNC43ODJDMTkuMjg0MyAxNC41OTAzIDE5LjU5MDMgMTQuMjg0MyAxOS43ODIgMTMuOTA4QzE5Ljg2MTcgMTMuNzUxNiAxOS45MjY2IDEzLjUyNzQgMTkuOTYyNCAxMy4wODlDMTkuOTk5MiAxMi42Mzg5IDIwIDEyLjA1NjYgMjAgMTEuMlY3LjhDMjAgNi45NDM0MiAxOS45OTkyIDYuMzYxMTMgMTkuOTYyNCA1LjkxMTA0QzE5LjkyNjYgNS40NzI2MiAxOS44NjE3IDUuMjQ4NDIgMTkuNzgyIDUuMDkyMDJDMTkuNTkwMyA0LjcxNTcgMTkuMjg0MyA0LjQwOTczIDE4LjkwOCA0LjIxNzk5QzE4Ljc1MTYgNC4xMzgzIDE4LjUyNzQgNC4wNzMzNyAxOC4wODkgNC4wMzc1NUMxNy42Mzg5IDQuMDAwNzggMTcuMDU2NiA0IDE2LjIgNEgxMi44QzExLjk0MzQgNCAxMS4zNjExIDQuMDAwNzggMTAuOTExIDQuMDM3NTVDMTAuNDcyNiA0LjA3MzM3IDEwLjI0ODQgNC4xMzgzIDEwLjA5MiA0LjIxNzk5QzkuNzE1NyA0LjQwOTczIDkuNDA5NzMgNC43MTU3IDkuMjE3OTkgNS4wOTIwMkM5LjEzODMgNS4yNDg0MiA5LjA3MzM3IDUuNDcyNjIgOS4wMzc1NSA1LjkxMTA0QzkuMDEzNTcgNi4yMDQ2MyA5LjAwNDg5IDYuNTU0NDcgOS4wMDE3NiA3Wk01LjkxMTA0IDkuMDM3NTVDNS40NzI2MiA5LjA3MzM3IDUuMjQ4NDIgOS4xMzgzIDUuMDkyMDIgOS4yMTc5OUM0LjcxNTcgOS40MDk3MyA0LjQwOTczIDkuNzE1NyA0LjIxNzk5IDEwLjA5MkM0LjEzODMgMTAuMjQ4NCA0LjA3MzM3IDEwLjQ3MjYgNC4wMzc1NSAxMC45MTFDNC4wMDA3OCAxMS4zNjExIDQgMTEuOTQzNCA0IDEyLjhWMTYuMkM0IDE3LjA1NjYgNC4wMDA3OCAxNy42Mzg5IDQuMDM3NTUgMTguMDg5QzQuMDczMzcgMTguNTI3NCA0LjEzODMgMTguNzUxNiA0LjIxNzk5IDE4LjkwOEM0LjQwOTczIDE5LjI4NDMgNC43MTU3IDE5LjU5MDMgNS4wOTIwMiAxOS43ODJDNS4yNDg0MiAxOS44NjE3IDUuNDcyNjIgMTkuOTI2NiA1LjkxMTA0IDE5Ljk2MjRDNi4zNjExMyAxOS45OTkyIDYuOTQzNDIgMjAgNy44IDIwSDExLjJDMTIuMDU2NiAyMCAxMi42Mzg5IDE5Ljk5OTIgMTMuMDg5IDE5Ljk2MjRDMTMuNTI3NCAxOS45MjY2IDEzLjc1MTYgMTkuODYxNyAxMy45MDggMTkuNzgyQzE0LjI4NDMgMTkuNTkwMyAxNC41OTAzIDE5LjI4NDMgMTQuNzgyIDE4LjkwOEMxNC44NjE3IDE4Ljc1MTYgMTQuOTI2NiAxOC41Mjc0IDE0Ljk2MjQgMTguMDg5QzE0Ljk5OTIgMTcuNjM4OSAxNSAxNy4wNTY2IDE1IDE2LjJWMTIuOEMxNSAxMS45NDM0IDE0Ljk5OTIgMTEuMzYxMSAxNC45NjI0IDEwLjkxMUMxNC45MjY2IDEwLjQ3MjYgMTQuODYxNyAxMC4yNDg0IDE0Ljc4MiAxMC4wOTJDMTQuNTkwMyA5LjcxNTcgMTQuMjg0MyA5LjQwOTczIDEzLjkwOCA5LjIxNzk5QzEzLjc1MTYgOS4xMzgzIDEzLjUyNzQgOS4wNzMzNyAxMy4wODkgOS4wMzc1NUMxMi42Mzg5IDkuMDAwNzggMTIuMDU2NiA5IDExLjIgOUg3LjhDNi45NDM0MiA5IDYuMzYxMTMgOS4wMDA3OCA1LjkxMTA0IDkuMDM3NTVaIiAvPjwvc3ZnPg==)]{._4jUWi
.pdMy8}]{.block .relative .w-[var(--button-icon-size)]
.h-[var(--button-icon-size)] transition-position="absolute"
style="--tg-will-change: transform, opacity; --tg-enter-opacity: 1; --tg-enter-transform: scale(1); --tg-enter-filter: none; --tg-enter-duration: 300ms; --tg-enter-delay: 150ms; --tg-enter-timing-function: var(--cubic-enter); --tg-exit-opacity: 0; --tg-exit-transform: scale(0.6); --tg-exit-filter: none; --tg-exit-duration: 150ms; --tg-exit-delay: 0ms; --tg-exit-timing-function: var(--cubic-exit); --tg-initial-opacity: 0; --tg-initial-transform: scale(0.6); --tg-initial-filter: none;"}]{.NBPKZ}
:::

``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
[
    {
        "id": "msg_67b73f697ba4819183a15cc17d011509",
        "type": "message",
        "role": "assistant",
        "content": [
            {
                "type": "output_text",
                "text": "Under the soft glow of the moon, Luna the unicorn danced through fields of twinkling stardust, leaving trails of dreams for every child asleep.",
                "annotations": []
            }
        ]
    }
]
```
::::
:::::

:::::::: Hrx2F
::::::: {.az2qq variant="outline" data-color="primary" actions-placement="end"}
::: rlGOC
![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxZW0iIGhlaWdodD0iMWVtIiBmaWxsPSJjdXJyZW50Q29sb3IiIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEzIDEyYTEgMSAwIDEgMC0yIDB2NGExIDEgMCAxIDAgMiAwdi00Wm0tMS0yLjVBMS4yNSAxLjI1IDAgMSAwIDEyIDdhMS4yNSAxLjI1IDAgMCAwIDAgMi41WiIgLz48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0xMiAyQzYuNDc3IDIgMiA2LjQ3NyAyIDEyczQuNDc3IDEwIDEwIDEwIDEwLTQuNDc3IDEwLTEwUzE3LjUyMyAyIDEyIDJaTTQgMTJhOCA4IDAgMSAxIDE2IDAgOCA4IDAgMCAxLTE2IDBaIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIC8+PC9zdmc+)
:::

::::: nCOFE
:::: QoPCW
::: VZYeX
**The `output` array often has more than one item in it!** It can
contain tool calls, data about reasoning tokens generated by [reasoning
models](/docs/guides/reasoning){.kZ98Q underline=""}, and other items.
It is not safe to assume that the model\'s text output is present at
`output[0].content[0].text`.
:::
::::
:::::
:::::::
::::::::

Some of our [official SDKs](/docs/libraries){.kZ98Q underline=""}
include an `output_text` property on model responses for convenience,
which aggregates all text outputs from the model into a single string.
This may be useful as a shortcut to access text output from the model.

In addition to plain text, you can also have the model return structured
data in JSON format - this feature is called [**Structured
Outputs**](/docs/guides/structured-outputs){.kZ98Q underline=""}.

::: anchor-heading-wrapper
## Prompt engineering![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjE1IiBoZWlnaHQ9IjE1IiBjbGFzcz0iYW5jaG9yLWhlYWRpbmctaWNvbiIgcm9sZT0icHJlc2VudGF0aW9uIj48cGF0aCBkPSJNMTguMjkyOSA1LjcwNzFDMTYuNDc0MyAzLjg4ODQ5IDEzLjUyNTcgMy44ODg0OSAxMS43MDcxIDUuNzA3MUwxMC43MDcxIDYuNzA3MUMxMC4zMTY2IDcuMDk3NjMgOS42ODM0MSA3LjA5NzYzIDkuMjkyODkgNi43MDcxQzguOTAyMzYgNi4zMTY1OCA4LjkwMjM2IDUuNjgzNDEgOS4yOTI4OSA1LjI5Mjg5TDEwLjI5MjkgNC4yOTI4OUMxMi44OTI2IDEuNjkzMjIgMTcuMTA3NCAxLjY5MzIyIDE5LjcwNzEgNC4yOTI4OUMyMi4zMDY4IDYuODkyNTUgMjIuMzA2OCAxMS4xMDc0IDE5LjcwNzEgMTMuNzA3MUwxOC43MDcxIDE0LjcwNzFDMTguMzE2NiAxNS4wOTc2IDE3LjY4MzQgMTUuMDk3NiAxNy4yOTI5IDE0LjcwNzFDMTYuOTAyNCAxNC4zMTY2IDE2LjkwMjQgMTMuNjgzNCAxNy4yOTI5IDEzLjI5MjlMMTguMjkyOSAxMi4yOTI5QzIwLjExMTUgMTAuNDc0MyAyMC4xMTE1IDcuNTI1NzIgMTguMjkyOSA1LjcwNzFaTTE1LjcwNzEgOC4yOTI4OUMxNi4wOTc2IDguNjgzNDEgMTYuMDk3NiA5LjMxNjU4IDE1LjcwNzEgOS43MDcxTDkuNzA3MSAxNS43MDcxQzkuMzE2NTggMTYuMDk3NiA4LjY4MzQxIDE2LjA5NzYgOC4yOTI4OSAxNS43MDcxQzcuOTAyMzYgMTUuMzE2NiA3LjkwMjM2IDE0LjY4MzQgOC4yOTI4OSAxNC4yOTI5TDE0LjI5MjkgOC4yOTI4OUMxNC42ODM0IDcuOTAyMzYgMTUuMzE2NiA3LjkwMjM2IDE1LjcwNzEgOC4yOTI4OVpNNi43MDcxIDkuMjkyODlDNy4wOTc2MyA5LjY4MzQxIDcuMDk3NjMgMTAuMzE2NiA2LjcwNzEgMTAuNzA3MUw1LjcwNzEgMTEuNzA3MUMzLjg4ODQ5IDEzLjUyNTcgMy44ODg0OSAxNi40NzQzIDUuNzA3MSAxOC4yOTI5QzcuNTI1NzIgMjAuMTExNSAxMC40NzQzIDIwLjExMTUgMTIuMjkyOSAxOC4yOTI5TDEzLjI5MjkgMTcuMjkyOUMxMy42ODM0IDE2LjkwMjQgMTQuMzE2NiAxNi45MDI0IDE0LjcwNzEgMTcuMjkyOUMxNS4wOTc2IDE3LjY4MzQgMTUuMDk3NiAxOC4zMTY2IDE0LjcwNzEgMTguNzA3MUwxMy43MDcxIDE5LjcwNzFDMTEuMTA3NCAyMi4zMDY4IDYuODkyNTUgMjIuMzA2OCA0LjI5Mjg5IDE5LjcwNzFDMS42OTMyMiAxNy4xMDc0IDEuNjkzMjIgMTIuODkyNiA0LjI5Mjg5IDEwLjI5MjlMNS4yOTI4OSA5LjI5Mjg5QzUuNjgzNDEgOC45MDIzNiA2LjMxNjU4IDguOTAyMzYgNi43MDcxIDkuMjkyODlaIiAvPjwvc3ZnPg==){.anchor-heading-icon} {#prompt-engineering .anchor-heading data-name="prompt-engineering"}
:::

**Prompt engineering** is the process of writing effective instructions
for a model, such that it consistently generates content that meets your
requirements.

Because the content generated from a model is non-deterministic,
prompting to get your desired output is a mix of art and science.
However, you can apply techniques and best practices to get good results
consistently.

Some prompt engineering techniques work with every model, like using
message roles. But different models might need to be prompted
differently to produce the best results. Even different snapshots of
models within the same family could produce different results. So as you
build more complex applications, we strongly recommend:

- Pinning your production applications to specific [model
  snapshots](/docs/models){.kZ98Q underline=""} (like `gpt-5-2025-08-07`
  for example) to ensure consistent behavior
- Building [evals](/docs/guides/evals){.kZ98Q underline=""} that measure
  the behavior of your prompts so you can monitor prompt performance as
  you iterate, or when you change and upgrade model versions

Now, let\'s examine some tools and techniques available to you to
construct prompts.

::: anchor-heading-wrapper
## Message roles and instruction following![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjE1IiBoZWlnaHQ9IjE1IiBjbGFzcz0iYW5jaG9yLWhlYWRpbmctaWNvbiIgcm9sZT0icHJlc2VudGF0aW9uIj48cGF0aCBkPSJNMTguMjkyOSA1LjcwNzFDMTYuNDc0MyAzLjg4ODQ5IDEzLjUyNTcgMy44ODg0OSAxMS43MDcxIDUuNzA3MUwxMC43MDcxIDYuNzA3MUMxMC4zMTY2IDcuMDk3NjMgOS42ODM0MSA3LjA5NzYzIDkuMjkyODkgNi43MDcxQzguOTAyMzYgNi4zMTY1OCA4LjkwMjM2IDUuNjgzNDEgOS4yOTI4OSA1LjI5Mjg5TDEwLjI5MjkgNC4yOTI4OUMxMi44OTI2IDEuNjkzMjIgMTcuMTA3NCAxLjY5MzIyIDE5LjcwNzEgNC4yOTI4OUMyMi4zMDY4IDYuODkyNTUgMjIuMzA2OCAxMS4xMDc0IDE5LjcwNzEgMTMuNzA3MUwxOC43MDcxIDE0LjcwNzFDMTguMzE2NiAxNS4wOTc2IDE3LjY4MzQgMTUuMDk3NiAxNy4yOTI5IDE0LjcwNzFDMTYuOTAyNCAxNC4zMTY2IDE2LjkwMjQgMTMuNjgzNCAxNy4yOTI5IDEzLjI5MjlMMTguMjkyOSAxMi4yOTI5QzIwLjExMTUgMTAuNDc0MyAyMC4xMTE1IDcuNTI1NzIgMTguMjkyOSA1LjcwNzFaTTE1LjcwNzEgOC4yOTI4OUMxNi4wOTc2IDguNjgzNDEgMTYuMDk3NiA5LjMxNjU4IDE1LjcwNzEgOS43MDcxTDkuNzA3MSAxNS43MDcxQzkuMzE2NTggMTYuMDk3NiA4LjY4MzQxIDE2LjA5NzYgOC4yOTI4OSAxNS43MDcxQzcuOTAyMzYgMTUuMzE2NiA3LjkwMjM2IDE0LjY4MzQgOC4yOTI4OSAxNC4yOTI5TDE0LjI5MjkgOC4yOTI4OUMxNC42ODM0IDcuOTAyMzYgMTUuMzE2NiA3LjkwMjM2IDE1LjcwNzEgOC4yOTI4OVpNNi43MDcxIDkuMjkyODlDNy4wOTc2MyA5LjY4MzQxIDcuMDk3NjMgMTAuMzE2NiA2LjcwNzEgMTAuNzA3MUw1LjcwNzEgMTEuNzA3MUMzLjg4ODQ5IDEzLjUyNTcgMy44ODg0OSAxNi40NzQzIDUuNzA3MSAxOC4yOTI5QzcuNTI1NzIgMjAuMTExNSAxMC40NzQzIDIwLjExMTUgMTIuMjkyOSAxOC4yOTI5TDEzLjI5MjkgMTcuMjkyOUMxMy42ODM0IDE2LjkwMjQgMTQuMzE2NiAxNi45MDI0IDE0LjcwNzEgMTcuMjkyOUMxNS4wOTc2IDE3LjY4MzQgMTUuMDk3NiAxOC4zMTY2IDE0LjcwNzEgMTguNzA3MUwxMy43MDcxIDE5LjcwNzFDMTEuMTA3NCAyMi4zMDY4IDYuODkyNTUgMjIuMzA2OCA0LjI5Mjg5IDE5LjcwNzFDMS42OTMyMiAxNy4xMDc0IDEuNjkzMjIgMTIuODkyNiA0LjI5Mjg5IDEwLjI5MjlMNS4yOTI4OSA5LjI5Mjg5QzUuNjgzNDEgOC45MDIzNiA2LjMxNjU4IDguOTAyMzYgNi43MDcxIDkuMjkyODlaIiAvPjwvc3ZnPg==){.anchor-heading-icon} {#message-roles-and-instruction-following .anchor-heading data-name="message-roles-and-instruction-following"}
:::

You can provide instructions to the model with [differing levels of
authority](https://model-spec.openai.com/2025-02-12.html#chain_of_command){.kZ98Q
target="_blank" rel="noopener noreferrer" underline=""} using the
`instructions` API parameter along with **message roles**.

The `instructions` parameter gives the model high-level instructions on
how it should behave while generating a response, including tone, goals,
and examples of correct responses. Any instructions provided this way
will take priority over a prompt in the `input` parameter.

::::::::::: {.code-sample .dark-mode}
:::::: code-sample-header
::: {.code-sample-title .body-small}
Generate text with instructions
:::

:::: exclude-from-copy
[[python]{.ktL9G}]{#select-trigger-:r11: .fsluc role="button"
tabindex="0" variant="ghost" data-size="sm" data-selected="true"
aria-disabled="false" type="button" aria-haspopup="dialog"
aria-expanded="false" aria-controls="radix-:r13:" state="closed"}

::: FJZOe
![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMWVtIiBoZWlnaHQ9IjFlbSIgdmlld2JveD0iMCAwIDEwIDE2IiBmaWxsPSJjdXJyZW50Q29sb3IiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgY2xhc3M9InlnenM2Ij48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTQuMzQxNTEgMC43NDc0MjNDNC43MTg1NCAwLjQxNzUyNiA1LjI4MTQ5IDAuNDE3NTI2IDUuNjU4NTIgMC43NDc0MjNMOS42NTg1MiA0LjI0NzQyQzEwLjA3NDIgNC42MTExMSAxMC4xMTYzIDUuMjQyODcgOS43NTI1OSA1LjY1ODVDOS4zODg5MSA2LjA3NDE0IDguNzU3MTUgNi4xMTYyNiA4LjM0MTUxIDUuNzUyNThMNS4wMDAwMSAyLjgyODc3TDEuNjU4NTIgNS43NTI1OEMxLjI0Mjg4IDYuMTE2MjYgMC42MTExMiA2LjA3NDE0IDAuMjQ3NDM4IDUuNjU4NUMtMC4xMTYyNDQgNS4yNDI4NyAtMC4wNzQxMjY3IDQuNjExMTEgMC4zNDE1MSA0LjI0NzQyTDQuMzQxNTEgMC43NDc0MjNaTTAuMjQ2MDY1IDEwLjM1NzhDMC42MDg4NzkgOS45NDEzOSAxLjI0MDU1IDkuODk3OTUgMS42NTY5NSAxMC4yNjA4TDUuMDAwMDEgMTMuMTczN0w4LjM0MzA4IDEwLjI2MDhDOC43NTk0OCA5Ljg5Nzk1IDkuMzkxMTUgOS45NDEzOSA5Ljc1Mzk2IDEwLjM1NzhDMTAuMTE2OCAxMC43NzQyIDEwLjA3MzMgMTEuNDA1OCA5LjY1Njk1IDExLjc2ODdMNS42NTY5NSAxNS4yNTM5QzUuMjgwNDMgMTUuNTgyIDQuNzE5NiAxNS41ODIgNC4zNDMwOCAxNS4yNTM5TDAuMzQzMDgyIDExLjc2ODdDLTAuMDczMzEyOCAxMS40MDU4IC0wLjExNjc0OSAxMC43NzQyIDAuMjQ2MDY1IDEwLjM1NzhaIiAvPjwvc3ZnPg==){.ygzs6}
:::
::::

[[[![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjFlbSIgaGVpZ2h0PSIxZW0iPjxwYXRoIGQ9Ik0xMi43NTg3IDJIMTYuMjQxM0MxNy4wNDYzIDEuOTk5OTkgMTcuNzEwNiAxLjk5OTk4IDE4LjI1MTggMi4wNDQxOUMxOC44MTM5IDIuMDkwMTIgMTkuMzMwNiAyLjE4ODY4IDE5LjgxNiAyLjQzNTk3QzIwLjU2ODYgMi44MTk0NyAyMS4xODA1IDMuNDMxMzkgMjEuNTY0IDQuMTg0MDRDMjEuODExMyA0LjY2OTM3IDIxLjkwOTkgNS4xODYwOCAyMS45NTU4IDUuNzQ4MTdDMjIgNi4yODkzNiAyMiA2Ljk1MzcyIDIyIDcuNzU4NjhWMTEuMjQxM0MyMiAxMi4wNDYzIDIyIDEyLjcxMDYgMjEuOTU1OCAxMy4yNTE4QzIxLjkwOTkgMTMuODEzOSAyMS44MTEzIDE0LjMzMDYgMjEuNTY0IDE0LjgxNkMyMS4xODA1IDE1LjU2ODYgMjAuNTY4NiAxNi4xODA1IDE5LjgxNiAxNi41NjRDMTkuMzMwNiAxNi44MTEzIDE4LjgxMzkgMTYuOTA5OSAxOC4yNTE4IDE2Ljk1NThDMTcuODkwNiAxNi45ODUzIDE3LjQ3NDUgMTYuOTk1MSAxNi45OTg0IDE2Ljk5ODRDMTYuOTk1MSAxNy40NzQ1IDE2Ljk4NTMgMTcuODkwNiAxNi45NTU4IDE4LjI1MThDMTYuOTA5OSAxOC44MTM5IDE2LjgxMTMgMTkuMzMwNiAxNi41NjQgMTkuODE2QzE2LjE4MDUgMjAuNTY4NiAxNS41Njg2IDIxLjE4MDUgMTQuODE2IDIxLjU2NEMxNC4zMzA2IDIxLjgxMTMgMTMuODEzOSAyMS45MDk5IDEzLjI1MTggMjEuOTU1OEMxMi43MTA2IDIyIDEyLjA0NjMgMjIgMTEuMjQxMyAyMkg3Ljc1ODY4QzYuOTUzNzIgMjIgNi4yODkzNiAyMiA1Ljc0ODE4IDIxLjk1NThDNS4xODYwOCAyMS45MDk5IDQuNjY5MzcgMjEuODExMyA0LjE4NDA0IDIxLjU2NEMzLjQzMTM5IDIxLjE4MDUgMi44MTk0NyAyMC41Njg2IDIuNDM1OTcgMTkuODE2QzIuMTg4NjggMTkuMzMwNiAyLjA5MDEyIDE4LjgxMzkgMi4wNDQxOSAxOC4yNTE4QzEuOTk5OTggMTcuNzEwNiAxLjk5OTk5IDE3LjA0NjMgMiAxNi4yNDEzVjEyLjc1ODdDMS45OTk5OSAxMS45NTM3IDEuOTk5OTggMTEuMjg5NCAyLjA0NDE5IDEwLjc0ODJDMi4wOTAxMiAxMC4xODYxIDIuMTg4NjggOS42NjkzNyAyLjQzNTk3IDkuMTg0MDRDMi44MTk0NyA4LjQzMTM5IDMuNDMxMzkgNy44MTk0NyA0LjE4NDA0IDcuNDM1OThDNC42NjkzNyA3LjE4ODY4IDUuMTg2MDggNy4wOTAxMiA1Ljc0ODE3IDcuMDQ0MTlDNi4xMDkzOSA3LjAxNDY4IDYuNTI1NDggNy4wMDQ4NyA3LjAwMTYyIDcuMDAxNjJDNy4wMDQ4NyA2LjUyNTQ4IDcuMDE0NjggNi4xMDkzOSA3LjA0NDE5IDUuNzQ4MTdDNy4wOTAxMiA1LjE4NjA4IDcuMTg4NjggNC42NjkzNyA3LjQzNTk4IDQuMTg0MDRDNy44MTk0NyAzLjQzMTM5IDguNDMxMzkgMi44MTk0NyA5LjE4NDA0IDIuNDM1OTdDOS42NjkzNyAyLjE4ODY4IDEwLjE4NjEgMi4wOTAxMiAxMC43NDgyIDIuMDQ0MTlDMTEuMjg5NCAxLjk5OTk4IDExLjk1MzcgMS45OTk5OSAxMi43NTg3IDJaTTkuMDAxNzYgN0wxMS4yNDEzIDdDMTIuMDQ2MyA2Ljk5OTk5IDEyLjcxMDYgNi45OTk5OCAxMy4yNTE4IDcuMDQ0MTlDMTMuODEzOSA3LjA5MDEyIDE0LjMzMDYgNy4xODg2OCAxNC44MTYgNy40MzU5OEMxNS41Njg2IDcuODE5NDcgMTYuMTgwNSA4LjQzMTM5IDE2LjU2NCA5LjE4NDA0QzE2LjgxMTMgOS42NjkzNyAxNi45MDk5IDEwLjE4NjEgMTYuOTU1OCAxMC43NDgyQzE3IDExLjI4OTQgMTcgMTEuOTUzNyAxNyAxMi43NTg3VjE0Ljk5ODJDMTcuNDQ1NSAxNC45OTUxIDE3Ljc5NTQgMTQuOTg2NCAxOC4wODkgMTQuOTYyNEMxOC41Mjc0IDE0LjkyNjYgMTguNzUxNiAxNC44NjE3IDE4LjkwOCAxNC43ODJDMTkuMjg0MyAxNC41OTAzIDE5LjU5MDMgMTQuMjg0MyAxOS43ODIgMTMuOTA4QzE5Ljg2MTcgMTMuNzUxNiAxOS45MjY2IDEzLjUyNzQgMTkuOTYyNCAxMy4wODlDMTkuOTk5MiAxMi42Mzg5IDIwIDEyLjA1NjYgMjAgMTEuMlY3LjhDMjAgNi45NDM0MiAxOS45OTkyIDYuMzYxMTMgMTkuOTYyNCA1LjkxMTA0QzE5LjkyNjYgNS40NzI2MiAxOS44NjE3IDUuMjQ4NDIgMTkuNzgyIDUuMDkyMDJDMTkuNTkwMyA0LjcxNTcgMTkuMjg0MyA0LjQwOTczIDE4LjkwOCA0LjIxNzk5QzE4Ljc1MTYgNC4xMzgzIDE4LjUyNzQgNC4wNzMzNyAxOC4wODkgNC4wMzc1NUMxNy42Mzg5IDQuMDAwNzggMTcuMDU2NiA0IDE2LjIgNEgxMi44QzExLjk0MzQgNCAxMS4zNjExIDQuMDAwNzggMTAuOTExIDQuMDM3NTVDMTAuNDcyNiA0LjA3MzM3IDEwLjI0ODQgNC4xMzgzIDEwLjA5MiA0LjIxNzk5QzkuNzE1NyA0LjQwOTczIDkuNDA5NzMgNC43MTU3IDkuMjE3OTkgNS4wOTIwMkM5LjEzODMgNS4yNDg0MiA5LjA3MzM3IDUuNDcyNjIgOS4wMzc1NSA1LjkxMTA0QzkuMDEzNTcgNi4yMDQ2MyA5LjAwNDg5IDYuNTU0NDcgOS4wMDE3NiA3Wk01LjkxMTA0IDkuMDM3NTVDNS40NzI2MiA5LjA3MzM3IDUuMjQ4NDIgOS4xMzgzIDUuMDkyMDIgOS4yMTc5OUM0LjcxNTcgOS40MDk3MyA0LjQwOTczIDkuNzE1NyA0LjIxNzk5IDEwLjA5MkM0LjEzODMgMTAuMjQ4NCA0LjA3MzM3IDEwLjQ3MjYgNC4wMzc1NSAxMC45MTFDNC4wMDA3OCAxMS4zNjExIDQgMTEuOTQzNCA0IDEyLjhWMTYuMkM0IDE3LjA1NjYgNC4wMDA3OCAxNy42Mzg5IDQuMDM3NTUgMTguMDg5QzQuMDczMzcgMTguNTI3NCA0LjEzODMgMTguNzUxNiA0LjIxNzk5IDE4LjkwOEM0LjQwOTczIDE5LjI4NDMgNC43MTU3IDE5LjU5MDMgNS4wOTIwMiAxOS43ODJDNS4yNDg0MiAxOS44NjE3IDUuNDcyNjIgMTkuOTI2NiA1LjkxMTA0IDE5Ljk2MjRDNi4zNjExMyAxOS45OTkyIDYuOTQzNDIgMjAgNy44IDIwSDExLjJDMTIuMDU2NiAyMCAxMi42Mzg5IDE5Ljk5OTIgMTMuMDg5IDE5Ljk2MjRDMTMuNTI3NCAxOS45MjY2IDEzLjc1MTYgMTkuODYxNyAxMy45MDggMTkuNzgyQzE0LjI4NDMgMTkuNTkwMyAxNC41OTAzIDE5LjI4NDMgMTQuNzgyIDE4LjkwOEMxNC44NjE3IDE4Ljc1MTYgMTQuOTI2NiAxOC41Mjc0IDE0Ljk2MjQgMTguMDg5QzE0Ljk5OTIgMTcuNjM4OSAxNSAxNy4wNTY2IDE1IDE2LjJWMTIuOEMxNSAxMS45NDM0IDE0Ljk5OTIgMTEuMzYxMSAxNC45NjI0IDEwLjkxMUMxNC45MjY2IDEwLjQ3MjYgMTQuODYxNyAxMC4yNDg0IDE0Ljc4MiAxMC4wOTJDMTQuNTkwMyA5LjcxNTcgMTQuMjg0MyA5LjQwOTczIDEzLjkwOCA5LjIxNzk5QzEzLjc1MTYgOS4xMzgzIDEzLjUyNzQgOS4wNzMzNyAxMy4wODkgOS4wMzc1NUMxMi42Mzg5IDkuMDAwNzggMTIuMDU2NiA5IDExLjIgOUg3LjhDNi45NDM0MiA5IDYuMzYxMTMgOS4wMDA3OCA1LjkxMTA0IDkuMDM3NTVaIiAvPjwvc3ZnPg==)]{._4jUWi
.pdMy8}]{.block .relative .w-[var(--button-icon-size)]
.h-[var(--button-icon-size)] transition-position="absolute"
style="--tg-will-change: transform, opacity; --tg-enter-opacity: 1; --tg-enter-transform: scale(1); --tg-enter-filter: none; --tg-enter-duration: 300ms; --tg-enter-delay: 150ms; --tg-enter-timing-function: var(--cubic-enter); --tg-exit-opacity: 0; --tg-exit-transform: scale(0.6); --tg-exit-filter: none; --tg-exit-duration: 150ms; --tg-exit-delay: 0ms; --tg-exit-timing-function: var(--cubic-exit); --tg-initial-opacity: 0; --tg-initial-transform: scale(0.6); --tg-initial-filter: none;"}]{.NBPKZ}
::::::

:::::: {.code-sample-body .code-sample-body-small .code-sample-body-with-header}
::: {.code-block .hidden}
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
10
11
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-5",
    reasoning: { effort: "low" },
    instructions: "Talk like a pirate.",
    input: "Are semicolons optional in JavaScript?",
});

console.log(response.output_text);
```
:::

::: code-block
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
10
11
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    reasoning={"effort": "low"},
    instructions="Talk like a pirate.",
    input="Are semicolons optional in JavaScript?",
)

print(response.output_text)
```
:::

::: {.code-block .hidden}
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-5",
        "reasoning": {"effort": "low"},
        "instructions": "Talk like a pirate.",
        "input": "Are semicolons optional in JavaScript?"
    }'
```
:::
::::::
:::::::::::

The example above is roughly equivalent to using the following input
messages in the `input` array:

::::::::::: {.code-sample .dark-mode}
:::::: code-sample-header
::: {.code-sample-title .body-small}
Generate text with messages using different roles
:::

:::: exclude-from-copy
[[python]{.ktL9G}]{#select-trigger-:r14: .fsluc role="button"
tabindex="0" variant="ghost" data-size="sm" data-selected="true"
aria-disabled="false" type="button" aria-haspopup="dialog"
aria-expanded="false" aria-controls="radix-:r16:" state="closed"}

::: FJZOe
![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMWVtIiBoZWlnaHQ9IjFlbSIgdmlld2JveD0iMCAwIDEwIDE2IiBmaWxsPSJjdXJyZW50Q29sb3IiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgY2xhc3M9InlnenM2Ij48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTQuMzQxNTEgMC43NDc0MjNDNC43MTg1NCAwLjQxNzUyNiA1LjI4MTQ5IDAuNDE3NTI2IDUuNjU4NTIgMC43NDc0MjNMOS42NTg1MiA0LjI0NzQyQzEwLjA3NDIgNC42MTExMSAxMC4xMTYzIDUuMjQyODcgOS43NTI1OSA1LjY1ODVDOS4zODg5MSA2LjA3NDE0IDguNzU3MTUgNi4xMTYyNiA4LjM0MTUxIDUuNzUyNThMNS4wMDAwMSAyLjgyODc3TDEuNjU4NTIgNS43NTI1OEMxLjI0Mjg4IDYuMTE2MjYgMC42MTExMiA2LjA3NDE0IDAuMjQ3NDM4IDUuNjU4NUMtMC4xMTYyNDQgNS4yNDI4NyAtMC4wNzQxMjY3IDQuNjExMTEgMC4zNDE1MSA0LjI0NzQyTDQuMzQxNTEgMC43NDc0MjNaTTAuMjQ2MDY1IDEwLjM1NzhDMC42MDg4NzkgOS45NDEzOSAxLjI0MDU1IDkuODk3OTUgMS42NTY5NSAxMC4yNjA4TDUuMDAwMDEgMTMuMTczN0w4LjM0MzA4IDEwLjI2MDhDOC43NTk0OCA5Ljg5Nzk1IDkuMzkxMTUgOS45NDEzOSA5Ljc1Mzk2IDEwLjM1NzhDMTAuMTE2OCAxMC43NzQyIDEwLjA3MzMgMTEuNDA1OCA5LjY1Njk1IDExLjc2ODdMNS42NTY5NSAxNS4yNTM5QzUuMjgwNDMgMTUuNTgyIDQuNzE5NiAxNS41ODIgNC4zNDMwOCAxNS4yNTM5TDAuMzQzMDgyIDExLjc2ODdDLTAuMDczMzEyOCAxMS40MDU4IC0wLjExNjc0OSAxMC43NzQyIDAuMjQ2MDY1IDEwLjM1NzhaIiAvPjwvc3ZnPg==){.ygzs6}
:::
::::

[[[![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjFlbSIgaGVpZ2h0PSIxZW0iPjxwYXRoIGQ9Ik0xMi43NTg3IDJIMTYuMjQxM0MxNy4wNDYzIDEuOTk5OTkgMTcuNzEwNiAxLjk5OTk4IDE4LjI1MTggMi4wNDQxOUMxOC44MTM5IDIuMDkwMTIgMTkuMzMwNiAyLjE4ODY4IDE5LjgxNiAyLjQzNTk3QzIwLjU2ODYgMi44MTk0NyAyMS4xODA1IDMuNDMxMzkgMjEuNTY0IDQuMTg0MDRDMjEuODExMyA0LjY2OTM3IDIxLjkwOTkgNS4xODYwOCAyMS45NTU4IDUuNzQ4MTdDMjIgNi4yODkzNiAyMiA2Ljk1MzcyIDIyIDcuNzU4NjhWMTEuMjQxM0MyMiAxMi4wNDYzIDIyIDEyLjcxMDYgMjEuOTU1OCAxMy4yNTE4QzIxLjkwOTkgMTMuODEzOSAyMS44MTEzIDE0LjMzMDYgMjEuNTY0IDE0LjgxNkMyMS4xODA1IDE1LjU2ODYgMjAuNTY4NiAxNi4xODA1IDE5LjgxNiAxNi41NjRDMTkuMzMwNiAxNi44MTEzIDE4LjgxMzkgMTYuOTA5OSAxOC4yNTE4IDE2Ljk1NThDMTcuODkwNiAxNi45ODUzIDE3LjQ3NDUgMTYuOTk1MSAxNi45OTg0IDE2Ljk5ODRDMTYuOTk1MSAxNy40NzQ1IDE2Ljk4NTMgMTcuODkwNiAxNi45NTU4IDE4LjI1MThDMTYuOTA5OSAxOC44MTM5IDE2LjgxMTMgMTkuMzMwNiAxNi41NjQgMTkuODE2QzE2LjE4MDUgMjAuNTY4NiAxNS41Njg2IDIxLjE4MDUgMTQuODE2IDIxLjU2NEMxNC4zMzA2IDIxLjgxMTMgMTMuODEzOSAyMS45MDk5IDEzLjI1MTggMjEuOTU1OEMxMi43MTA2IDIyIDEyLjA0NjMgMjIgMTEuMjQxMyAyMkg3Ljc1ODY4QzYuOTUzNzIgMjIgNi4yODkzNiAyMiA1Ljc0ODE4IDIxLjk1NThDNS4xODYwOCAyMS45MDk5IDQuNjY5MzcgMjEuODExMyA0LjE4NDA0IDIxLjU2NEMzLjQzMTM5IDIxLjE4MDUgMi44MTk0NyAyMC41Njg2IDIuNDM1OTcgMTkuODE2QzIuMTg4NjggMTkuMzMwNiAyLjA5MDEyIDE4LjgxMzkgMi4wNDQxOSAxOC4yNTE4QzEuOTk5OTggMTcuNzEwNiAxLjk5OTk5IDE3LjA0NjMgMiAxNi4yNDEzVjEyLjc1ODdDMS45OTk5OSAxMS45NTM3IDEuOTk5OTggMTEuMjg5NCAyLjA0NDE5IDEwLjc0ODJDMi4wOTAxMiAxMC4xODYxIDIuMTg4NjggOS42NjkzNyAyLjQzNTk3IDkuMTg0MDRDMi44MTk0NyA4LjQzMTM5IDMuNDMxMzkgNy44MTk0NyA0LjE4NDA0IDcuNDM1OThDNC42NjkzNyA3LjE4ODY4IDUuMTg2MDggNy4wOTAxMiA1Ljc0ODE3IDcuMDQ0MTlDNi4xMDkzOSA3LjAxNDY4IDYuNTI1NDggNy4wMDQ4NyA3LjAwMTYyIDcuMDAxNjJDNy4wMDQ4NyA2LjUyNTQ4IDcuMDE0NjggNi4xMDkzOSA3LjA0NDE5IDUuNzQ4MTdDNy4wOTAxMiA1LjE4NjA4IDcuMTg4NjggNC42NjkzNyA3LjQzNTk4IDQuMTg0MDRDNy44MTk0NyAzLjQzMTM5IDguNDMxMzkgMi44MTk0NyA5LjE4NDA0IDIuNDM1OTdDOS42NjkzNyAyLjE4ODY4IDEwLjE4NjEgMi4wOTAxMiAxMC43NDgyIDIuMDQ0MTlDMTEuMjg5NCAxLjk5OTk4IDExLjk1MzcgMS45OTk5OSAxMi43NTg3IDJaTTkuMDAxNzYgN0wxMS4yNDEzIDdDMTIuMDQ2MyA2Ljk5OTk5IDEyLjcxMDYgNi45OTk5OCAxMy4yNTE4IDcuMDQ0MTlDMTMuODEzOSA3LjA5MDEyIDE0LjMzMDYgNy4xODg2OCAxNC44MTYgNy40MzU5OEMxNS41Njg2IDcuODE5NDcgMTYuMTgwNSA4LjQzMTM5IDE2LjU2NCA5LjE4NDA0QzE2LjgxMTMgOS42NjkzNyAxNi45MDk5IDEwLjE4NjEgMTYuOTU1OCAxMC43NDgyQzE3IDExLjI4OTQgMTcgMTEuOTUzNyAxNyAxMi43NTg3VjE0Ljk5ODJDMTcuNDQ1NSAxNC45OTUxIDE3Ljc5NTQgMTQuOTg2NCAxOC4wODkgMTQuOTYyNEMxOC41Mjc0IDE0LjkyNjYgMTguNzUxNiAxNC44NjE3IDE4LjkwOCAxNC43ODJDMTkuMjg0MyAxNC41OTAzIDE5LjU5MDMgMTQuMjg0MyAxOS43ODIgMTMuOTA4QzE5Ljg2MTcgMTMuNzUxNiAxOS45MjY2IDEzLjUyNzQgMTkuOTYyNCAxMy4wODlDMTkuOTk5MiAxMi42Mzg5IDIwIDEyLjA1NjYgMjAgMTEuMlY3LjhDMjAgNi45NDM0MiAxOS45OTkyIDYuMzYxMTMgMTkuOTYyNCA1LjkxMTA0QzE5LjkyNjYgNS40NzI2MiAxOS44NjE3IDUuMjQ4NDIgMTkuNzgyIDUuMDkyMDJDMTkuNTkwMyA0LjcxNTcgMTkuMjg0MyA0LjQwOTczIDE4LjkwOCA0LjIxNzk5QzE4Ljc1MTYgNC4xMzgzIDE4LjUyNzQgNC4wNzMzNyAxOC4wODkgNC4wMzc1NUMxNy42Mzg5IDQuMDAwNzggMTcuMDU2NiA0IDE2LjIgNEgxMi44QzExLjk0MzQgNCAxMS4zNjExIDQuMDAwNzggMTAuOTExIDQuMDM3NTVDMTAuNDcyNiA0LjA3MzM3IDEwLjI0ODQgNC4xMzgzIDEwLjA5MiA0LjIxNzk5QzkuNzE1NyA0LjQwOTczIDkuNDA5NzMgNC43MTU3IDkuMjE3OTkgNS4wOTIwMkM5LjEzODMgNS4yNDg0MiA5LjA3MzM3IDUuNDcyNjIgOS4wMzc1NSA1LjkxMTA0QzkuMDEzNTcgNi4yMDQ2MyA5LjAwNDg5IDYuNTU0NDcgOS4wMDE3NiA3Wk01LjkxMTA0IDkuMDM3NTVDNS40NzI2MiA5LjA3MzM3IDUuMjQ4NDIgOS4xMzgzIDUuMDkyMDIgOS4yMTc5OUM0LjcxNTcgOS40MDk3MyA0LjQwOTczIDkuNzE1NyA0LjIxNzk5IDEwLjA5MkM0LjEzODMgMTAuMjQ4NCA0LjA3MzM3IDEwLjQ3MjYgNC4wMzc1NSAxMC45MTFDNC4wMDA3OCAxMS4zNjExIDQgMTEuOTQzNCA0IDEyLjhWMTYuMkM0IDE3LjA1NjYgNC4wMDA3OCAxNy42Mzg5IDQuMDM3NTUgMTguMDg5QzQuMDczMzcgMTguNTI3NCA0LjEzODMgMTguNzUxNiA0LjIxNzk5IDE4LjkwOEM0LjQwOTczIDE5LjI4NDMgNC43MTU3IDE5LjU5MDMgNS4wOTIwMiAxOS43ODJDNS4yNDg0MiAxOS44NjE3IDUuNDcyNjIgMTkuOTI2NiA1LjkxMTA0IDE5Ljk2MjRDNi4zNjExMyAxOS45OTkyIDYuOTQzNDIgMjAgNy44IDIwSDExLjJDMTIuMDU2NiAyMCAxMi42Mzg5IDE5Ljk5OTIgMTMuMDg5IDE5Ljk2MjRDMTMuNTI3NCAxOS45MjY2IDEzLjc1MTYgMTkuODYxNyAxMy45MDggMTkuNzgyQzE0LjI4NDMgMTkuNTkwMyAxNC41OTAzIDE5LjI4NDMgMTQuNzgyIDE4LjkwOEMxNC44NjE3IDE4Ljc1MTYgMTQuOTI2NiAxOC41Mjc0IDE0Ljk2MjQgMTguMDg5QzE0Ljk5OTIgMTcuNjM4OSAxNSAxNy4wNTY2IDE1IDE2LjJWMTIuOEMxNSAxMS45NDM0IDE0Ljk5OTIgMTEuMzYxMSAxNC45NjI0IDEwLjkxMUMxNC45MjY2IDEwLjQ3MjYgMTQuODYxNyAxMC4yNDg0IDE0Ljc4MiAxMC4wOTJDMTQuNTkwMyA5LjcxNTcgMTQuMjg0MyA5LjQwOTczIDEzLjkwOCA5LjIxNzk5QzEzLjc1MTYgOS4xMzgzIDEzLjUyNzQgOS4wNzMzNyAxMy4wODkgOS4wMzc1NUMxMi42Mzg5IDkuMDAwNzggMTIuMDU2NiA5IDExLjIgOUg3LjhDNi45NDM0MiA5IDYuMzYxMTMgOS4wMDA3OCA1LjkxMTA0IDkuMDM3NTVaIiAvPjwvc3ZnPg==)]{._4jUWi
.pdMy8}]{.block .relative .w-[var(--button-icon-size)]
.h-[var(--button-icon-size)] transition-position="absolute"
style="--tg-will-change: transform, opacity; --tg-enter-opacity: 1; --tg-enter-transform: scale(1); --tg-enter-filter: none; --tg-enter-duration: 300ms; --tg-enter-delay: 150ms; --tg-enter-timing-function: var(--cubic-enter); --tg-exit-opacity: 0; --tg-exit-transform: scale(0.6); --tg-exit-filter: none; --tg-exit-duration: 150ms; --tg-exit-delay: 0ms; --tg-exit-timing-function: var(--cubic-exit); --tg-initial-opacity: 0; --tg-initial-transform: scale(0.6); --tg-initial-filter: none;"}]{.NBPKZ}
::::::

:::::: {.code-sample-body .code-sample-body-small .code-sample-body-with-header}
::: {.code-block .hidden}
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-5",
    reasoning: { effort: "low" },
    input: [
        {
            role: "developer",
            content: "Talk like a pirate."
        },
        {
            role: "user",
            content: "Are semicolons optional in JavaScript?",
        },
    ],
});

console.log(response.output_text);
```
:::

::: code-block
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    reasoning={"effort": "low"},
    input=[
        {
            "role": "developer",
            "content": "Talk like a pirate."
        },
        {
            "role": "user",
            "content": "Are semicolons optional in JavaScript?"
        }
    ]
)

print(response.output_text)
```
:::

::: {.code-block .hidden}
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-5",
        "reasoning": {"effort": "low"},
        "input": [
            {
                "role": "developer",
                "content": "Talk like a pirate."
            },
            {
                "role": "user",
                "content": "Are semicolons optional in JavaScript?"
            }
        ]
    }'
```
:::
::::::
:::::::::::

:::::::: Hrx2F
::::::: {.az2qq variant="outline" data-color="primary" actions-placement="end"}
::: rlGOC
![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxZW0iIGhlaWdodD0iMWVtIiBmaWxsPSJjdXJyZW50Q29sb3IiIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEzIDEyYTEgMSAwIDEgMC0yIDB2NGExIDEgMCAxIDAgMiAwdi00Wm0tMS0yLjVBMS4yNSAxLjI1IDAgMSAwIDEyIDdhMS4yNSAxLjI1IDAgMCAwIDAgMi41WiIgLz48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0xMiAyQzYuNDc3IDIgMiA2LjQ3NyAyIDEyczQuNDc3IDEwIDEwIDEwIDEwLTQuNDc3IDEwLTEwUzE3LjUyMyAyIDEyIDJaTTQgMTJhOCA4IDAgMSAxIDE2IDAgOCA4IDAgMCAxLTE2IDBaIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIC8+PC9zdmc+)
:::

::::: nCOFE
:::: QoPCW
::: VZYeX
Note that the `instructions` parameter only applies to the current
response generation request. If you are [managing conversation
state](/docs/guides/conversation-state){.kZ98Q underline=""} with the
`previous_response_id` parameter, the `instructions` used on previous
turns will not be present in the context.
:::
::::
:::::
:::::::
::::::::

The [OpenAI model
spec](https://model-spec.openai.com/2025-02-12.html#chain_of_command){.kZ98Q
target="_blank" rel="noopener noreferrer" underline=""} describes how
our models give different levels of priority to messages with different
roles.

  developer                                                                                                          user                                                                                               assistant
  ------------------------------------------------------------------------------------------------------------------ -------------------------------------------------------------------------------------------------- ------------------------------------------------------------
  `developer` messages are instructions provided by the application developer, prioritized ahead of user messages.   `user` messages are instructions provided by an end user, prioritized behind developer messages.   Messages generated by the model have the `assistant` role.

A multi-turn conversation may consist of several messages of these
types, along with other content types provided by both you and the
model. Learn more about [managing conversation state
here](/docs/guides/conversation-state){.kZ98Q underline=""}.

You could think about `developer` and `user` messages like a function
and its arguments in a programming language.

- `developer` messages provide the system\'s rules and business logic,
  like a function definition.
- `user` messages provide inputs and configuration to which the
  `developer` message instructions are applied, like arguments to a
  function.

::: anchor-heading-wrapper
## Reusable prompts![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjE1IiBoZWlnaHQ9IjE1IiBjbGFzcz0iYW5jaG9yLWhlYWRpbmctaWNvbiIgcm9sZT0icHJlc2VudGF0aW9uIj48cGF0aCBkPSJNMTguMjkyOSA1LjcwNzFDMTYuNDc0MyAzLjg4ODQ5IDEzLjUyNTcgMy44ODg0OSAxMS43MDcxIDUuNzA3MUwxMC43MDcxIDYuNzA3MUMxMC4zMTY2IDcuMDk3NjMgOS42ODM0MSA3LjA5NzYzIDkuMjkyODkgNi43MDcxQzguOTAyMzYgNi4zMTY1OCA4LjkwMjM2IDUuNjgzNDEgOS4yOTI4OSA1LjI5Mjg5TDEwLjI5MjkgNC4yOTI4OUMxMi44OTI2IDEuNjkzMjIgMTcuMTA3NCAxLjY5MzIyIDE5LjcwNzEgNC4yOTI4OUMyMi4zMDY4IDYuODkyNTUgMjIuMzA2OCAxMS4xMDc0IDE5LjcwNzEgMTMuNzA3MUwxOC43MDcxIDE0LjcwNzFDMTguMzE2NiAxNS4wOTc2IDE3LjY4MzQgMTUuMDk3NiAxNy4yOTI5IDE0LjcwNzFDMTYuOTAyNCAxNC4zMTY2IDE2LjkwMjQgMTMuNjgzNCAxNy4yOTI5IDEzLjI5MjlMMTguMjkyOSAxMi4yOTI5QzIwLjExMTUgMTAuNDc0MyAyMC4xMTE1IDcuNTI1NzIgMTguMjkyOSA1LjcwNzFaTTE1LjcwNzEgOC4yOTI4OUMxNi4wOTc2IDguNjgzNDEgMTYuMDk3NiA5LjMxNjU4IDE1LjcwNzEgOS43MDcxTDkuNzA3MSAxNS43MDcxQzkuMzE2NTggMTYuMDk3NiA4LjY4MzQxIDE2LjA5NzYgOC4yOTI4OSAxNS43MDcxQzcuOTAyMzYgMTUuMzE2NiA3LjkwMjM2IDE0LjY4MzQgOC4yOTI4OSAxNC4yOTI5TDE0LjI5MjkgOC4yOTI4OUMxNC42ODM0IDcuOTAyMzYgMTUuMzE2NiA3LjkwMjM2IDE1LjcwNzEgOC4yOTI4OVpNNi43MDcxIDkuMjkyODlDNy4wOTc2MyA5LjY4MzQxIDcuMDk3NjMgMTAuMzE2NiA2LjcwNzEgMTAuNzA3MUw1LjcwNzEgMTEuNzA3MUMzLjg4ODQ5IDEzLjUyNTcgMy44ODg0OSAxNi40NzQzIDUuNzA3MSAxOC4yOTI5QzcuNTI1NzIgMjAuMTExNSAxMC40NzQzIDIwLjExMTUgMTIuMjkyOSAxOC4yOTI5TDEzLjI5MjkgMTcuMjkyOUMxMy42ODM0IDE2LjkwMjQgMTQuMzE2NiAxNi45MDI0IDE0LjcwNzEgMTcuMjkyOUMxNS4wOTc2IDE3LjY4MzQgMTUuMDk3NiAxOC4zMTY2IDE0LjcwNzEgMTguNzA3MUwxMy43MDcxIDE5LjcwNzFDMTEuMTA3NCAyMi4zMDY4IDYuODkyNTUgMjIuMzA2OCA0LjI5Mjg5IDE5LjcwNzFDMS42OTMyMiAxNy4xMDc0IDEuNjkzMjIgMTIuODkyNiA0LjI5Mjg5IDEwLjI5MjlMNS4yOTI4OSA5LjI5Mjg5QzUuNjgzNDEgOC45MDIzNiA2LjMxNjU4IDguOTAyMzYgNi43MDcxIDkuMjkyODlaIiAvPjwvc3ZnPg==){.anchor-heading-icon} {#reusable-prompts .anchor-heading data-name="reusable-prompts"}
:::

In the OpenAI dashboard, you can develop reusable
[prompts](/chat/edit){.kZ98Q underline=""} that you can use in API
requests, rather than specifying the content of prompts in code. This
way, you can more easily build and evaluate your prompts, and deploy
improved versions of your prompts without changing your integration
code.

Here\'s how it works:

1.  **Create a reusable prompt** in the [dashboard](/chat/edit){.kZ98Q
    underline=""} with placeholders like `{{customer_name}}`.
2.  **Use the prompt** in your API request with the `prompt` parameter.
    The prompt parameter object has three properties you can configure:
    - `id` --- Unique identifier of your prompt, found in the dashboard
    - `version` --- A specific version of your prompt (defaults to the
      \"current\" version as specified in the dashboard)
    - `variables` --- A map of values to substitute in for variables in
      your prompt. The substitution values can either be strings, or
      other Response input message types like `input_image` or
      `input_file`. [See the full API
      reference](/docs/api-reference/responses/create){.kZ98Q
      underline=""}.

:::::::::::::::::::::::::::::: mt-6
::::: {.exclude-from-copy .mb-6}
:::: {.F5Sy7 role="group" dir="ltr" data-size="md" aria-label="Content switcher" tabindex="0" style="outline: none;"}
::: {.V5HTp style="width: 124px; transform: translateX(2px); transition: width 300ms var(--cubic-enter), transform 300ms var(--cubic-enter);"}
:::

[String variables]{.relative}

[Variables with file input]{.relative}
::::
:::::

<div>

::: hidden
String variables
:::

<div>

::::::::::: {.code-sample .dark-mode}
:::::: code-sample-header
::: {.code-sample-title .body-small}
Generate text with a prompt template
:::

:::: exclude-from-copy
[[python]{.ktL9G}]{#select-trigger-:r19: .fsluc role="button"
tabindex="0" variant="ghost" data-size="sm" data-selected="true"
aria-disabled="false" type="button" aria-haspopup="dialog"
aria-expanded="false" aria-controls="radix-:r1b:" state="closed"}

::: FJZOe
![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMWVtIiBoZWlnaHQ9IjFlbSIgdmlld2JveD0iMCAwIDEwIDE2IiBmaWxsPSJjdXJyZW50Q29sb3IiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgY2xhc3M9InlnenM2Ij48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTQuMzQxNTEgMC43NDc0MjNDNC43MTg1NCAwLjQxNzUyNiA1LjI4MTQ5IDAuNDE3NTI2IDUuNjU4NTIgMC43NDc0MjNMOS42NTg1MiA0LjI0NzQyQzEwLjA3NDIgNC42MTExMSAxMC4xMTYzIDUuMjQyODcgOS43NTI1OSA1LjY1ODVDOS4zODg5MSA2LjA3NDE0IDguNzU3MTUgNi4xMTYyNiA4LjM0MTUxIDUuNzUyNThMNS4wMDAwMSAyLjgyODc3TDEuNjU4NTIgNS43NTI1OEMxLjI0Mjg4IDYuMTE2MjYgMC42MTExMiA2LjA3NDE0IDAuMjQ3NDM4IDUuNjU4NUMtMC4xMTYyNDQgNS4yNDI4NyAtMC4wNzQxMjY3IDQuNjExMTEgMC4zNDE1MSA0LjI0NzQyTDQuMzQxNTEgMC43NDc0MjNaTTAuMjQ2MDY1IDEwLjM1NzhDMC42MDg4NzkgOS45NDEzOSAxLjI0MDU1IDkuODk3OTUgMS42NTY5NSAxMC4yNjA4TDUuMDAwMDEgMTMuMTczN0w4LjM0MzA4IDEwLjI2MDhDOC43NTk0OCA5Ljg5Nzk1IDkuMzkxMTUgOS45NDEzOSA5Ljc1Mzk2IDEwLjM1NzhDMTAuMTE2OCAxMC43NzQyIDEwLjA3MzMgMTEuNDA1OCA5LjY1Njk1IDExLjc2ODdMNS42NTY5NSAxNS4yNTM5QzUuMjgwNDMgMTUuNTgyIDQuNzE5NiAxNS41ODIgNC4zNDMwOCAxNS4yNTM5TDAuMzQzMDgyIDExLjc2ODdDLTAuMDczMzEyOCAxMS40MDU4IC0wLjExNjc0OSAxMC43NzQyIDAuMjQ2MDY1IDEwLjM1NzhaIiAvPjwvc3ZnPg==){.ygzs6}
:::
::::

[[[![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjFlbSIgaGVpZ2h0PSIxZW0iPjxwYXRoIGQ9Ik0xMi43NTg3IDJIMTYuMjQxM0MxNy4wNDYzIDEuOTk5OTkgMTcuNzEwNiAxLjk5OTk4IDE4LjI1MTggMi4wNDQxOUMxOC44MTM5IDIuMDkwMTIgMTkuMzMwNiAyLjE4ODY4IDE5LjgxNiAyLjQzNTk3QzIwLjU2ODYgMi44MTk0NyAyMS4xODA1IDMuNDMxMzkgMjEuNTY0IDQuMTg0MDRDMjEuODExMyA0LjY2OTM3IDIxLjkwOTkgNS4xODYwOCAyMS45NTU4IDUuNzQ4MTdDMjIgNi4yODkzNiAyMiA2Ljk1MzcyIDIyIDcuNzU4NjhWMTEuMjQxM0MyMiAxMi4wNDYzIDIyIDEyLjcxMDYgMjEuOTU1OCAxMy4yNTE4QzIxLjkwOTkgMTMuODEzOSAyMS44MTEzIDE0LjMzMDYgMjEuNTY0IDE0LjgxNkMyMS4xODA1IDE1LjU2ODYgMjAuNTY4NiAxNi4xODA1IDE5LjgxNiAxNi41NjRDMTkuMzMwNiAxNi44MTEzIDE4LjgxMzkgMTYuOTA5OSAxOC4yNTE4IDE2Ljk1NThDMTcuODkwNiAxNi45ODUzIDE3LjQ3NDUgMTYuOTk1MSAxNi45OTg0IDE2Ljk5ODRDMTYuOTk1MSAxNy40NzQ1IDE2Ljk4NTMgMTcuODkwNiAxNi45NTU4IDE4LjI1MThDMTYuOTA5OSAxOC44MTM5IDE2LjgxMTMgMTkuMzMwNiAxNi41NjQgMTkuODE2QzE2LjE4MDUgMjAuNTY4NiAxNS41Njg2IDIxLjE4MDUgMTQuODE2IDIxLjU2NEMxNC4zMzA2IDIxLjgxMTMgMTMuODEzOSAyMS45MDk5IDEzLjI1MTggMjEuOTU1OEMxMi43MTA2IDIyIDEyLjA0NjMgMjIgMTEuMjQxMyAyMkg3Ljc1ODY4QzYuOTUzNzIgMjIgNi4yODkzNiAyMiA1Ljc0ODE4IDIxLjk1NThDNS4xODYwOCAyMS45MDk5IDQuNjY5MzcgMjEuODExMyA0LjE4NDA0IDIxLjU2NEMzLjQzMTM5IDIxLjE4MDUgMi44MTk0NyAyMC41Njg2IDIuNDM1OTcgMTkuODE2QzIuMTg4NjggMTkuMzMwNiAyLjA5MDEyIDE4LjgxMzkgMi4wNDQxOSAxOC4yNTE4QzEuOTk5OTggMTcuNzEwNiAxLjk5OTk5IDE3LjA0NjMgMiAxNi4yNDEzVjEyLjc1ODdDMS45OTk5OSAxMS45NTM3IDEuOTk5OTggMTEuMjg5NCAyLjA0NDE5IDEwLjc0ODJDMi4wOTAxMiAxMC4xODYxIDIuMTg4NjggOS42NjkzNyAyLjQzNTk3IDkuMTg0MDRDMi44MTk0NyA4LjQzMTM5IDMuNDMxMzkgNy44MTk0NyA0LjE4NDA0IDcuNDM1OThDNC42NjkzNyA3LjE4ODY4IDUuMTg2MDggNy4wOTAxMiA1Ljc0ODE3IDcuMDQ0MTlDNi4xMDkzOSA3LjAxNDY4IDYuNTI1NDggNy4wMDQ4NyA3LjAwMTYyIDcuMDAxNjJDNy4wMDQ4NyA2LjUyNTQ4IDcuMDE0NjggNi4xMDkzOSA3LjA0NDE5IDUuNzQ4MTdDNy4wOTAxMiA1LjE4NjA4IDcuMTg4NjggNC42NjkzNyA3LjQzNTk4IDQuMTg0MDRDNy44MTk0NyAzLjQzMTM5IDguNDMxMzkgMi44MTk0NyA5LjE4NDA0IDIuNDM1OTdDOS42NjkzNyAyLjE4ODY4IDEwLjE4NjEgMi4wOTAxMiAxMC43NDgyIDIuMDQ0MTlDMTEuMjg5NCAxLjk5OTk4IDExLjk1MzcgMS45OTk5OSAxMi43NTg3IDJaTTkuMDAxNzYgN0wxMS4yNDEzIDdDMTIuMDQ2MyA2Ljk5OTk5IDEyLjcxMDYgNi45OTk5OCAxMy4yNTE4IDcuMDQ0MTlDMTMuODEzOSA3LjA5MDEyIDE0LjMzMDYgNy4xODg2OCAxNC44MTYgNy40MzU5OEMxNS41Njg2IDcuODE5NDcgMTYuMTgwNSA4LjQzMTM5IDE2LjU2NCA5LjE4NDA0QzE2LjgxMTMgOS42NjkzNyAxNi45MDk5IDEwLjE4NjEgMTYuOTU1OCAxMC43NDgyQzE3IDExLjI4OTQgMTcgMTEuOTUzNyAxNyAxMi43NTg3VjE0Ljk5ODJDMTcuNDQ1NSAxNC45OTUxIDE3Ljc5NTQgMTQuOTg2NCAxOC4wODkgMTQuOTYyNEMxOC41Mjc0IDE0LjkyNjYgMTguNzUxNiAxNC44NjE3IDE4LjkwOCAxNC43ODJDMTkuMjg0MyAxNC41OTAzIDE5LjU5MDMgMTQuMjg0MyAxOS43ODIgMTMuOTA4QzE5Ljg2MTcgMTMuNzUxNiAxOS45MjY2IDEzLjUyNzQgMTkuOTYyNCAxMy4wODlDMTkuOTk5MiAxMi42Mzg5IDIwIDEyLjA1NjYgMjAgMTEuMlY3LjhDMjAgNi45NDM0MiAxOS45OTkyIDYuMzYxMTMgMTkuOTYyNCA1LjkxMTA0QzE5LjkyNjYgNS40NzI2MiAxOS44NjE3IDUuMjQ4NDIgMTkuNzgyIDUuMDkyMDJDMTkuNTkwMyA0LjcxNTcgMTkuMjg0MyA0LjQwOTczIDE4LjkwOCA0LjIxNzk5QzE4Ljc1MTYgNC4xMzgzIDE4LjUyNzQgNC4wNzMzNyAxOC4wODkgNC4wMzc1NUMxNy42Mzg5IDQuMDAwNzggMTcuMDU2NiA0IDE2LjIgNEgxMi44QzExLjk0MzQgNCAxMS4zNjExIDQuMDAwNzggMTAuOTExIDQuMDM3NTVDMTAuNDcyNiA0LjA3MzM3IDEwLjI0ODQgNC4xMzgzIDEwLjA5MiA0LjIxNzk5QzkuNzE1NyA0LjQwOTczIDkuNDA5NzMgNC43MTU3IDkuMjE3OTkgNS4wOTIwMkM5LjEzODMgNS4yNDg0MiA5LjA3MzM3IDUuNDcyNjIgOS4wMzc1NSA1LjkxMTA0QzkuMDEzNTcgNi4yMDQ2MyA5LjAwNDg5IDYuNTU0NDcgOS4wMDE3NiA3Wk01LjkxMTA0IDkuMDM3NTVDNS40NzI2MiA5LjA3MzM3IDUuMjQ4NDIgOS4xMzgzIDUuMDkyMDIgOS4yMTc5OUM0LjcxNTcgOS40MDk3MyA0LjQwOTczIDkuNzE1NyA0LjIxNzk5IDEwLjA5MkM0LjEzODMgMTAuMjQ4NCA0LjA3MzM3IDEwLjQ3MjYgNC4wMzc1NSAxMC45MTFDNC4wMDA3OCAxMS4zNjExIDQgMTEuOTQzNCA0IDEyLjhWMTYuMkM0IDE3LjA1NjYgNC4wMDA3OCAxNy42Mzg5IDQuMDM3NTUgMTguMDg5QzQuMDczMzcgMTguNTI3NCA0LjEzODMgMTguNzUxNiA0LjIxNzk5IDE4LjkwOEM0LjQwOTczIDE5LjI4NDMgNC43MTU3IDE5LjU5MDMgNS4wOTIwMiAxOS43ODJDNS4yNDg0MiAxOS44NjE3IDUuNDcyNjIgMTkuOTI2NiA1LjkxMTA0IDE5Ljk2MjRDNi4zNjExMyAxOS45OTkyIDYuOTQzNDIgMjAgNy44IDIwSDExLjJDMTIuMDU2NiAyMCAxMi42Mzg5IDE5Ljk5OTIgMTMuMDg5IDE5Ljk2MjRDMTMuNTI3NCAxOS45MjY2IDEzLjc1MTYgMTkuODYxNyAxMy45MDggMTkuNzgyQzE0LjI4NDMgMTkuNTkwMyAxNC41OTAzIDE5LjI4NDMgMTQuNzgyIDE4LjkwOEMxNC44NjE3IDE4Ljc1MTYgMTQuOTI2NiAxOC41Mjc0IDE0Ljk2MjQgMTguMDg5QzE0Ljk5OTIgMTcuNjM4OSAxNSAxNy4wNTY2IDE1IDE2LjJWMTIuOEMxNSAxMS45NDM0IDE0Ljk5OTIgMTEuMzYxMSAxNC45NjI0IDEwLjkxMUMxNC45MjY2IDEwLjQ3MjYgMTQuODYxNyAxMC4yNDg0IDE0Ljc4MiAxMC4wOTJDMTQuNTkwMyA5LjcxNTcgMTQuMjg0MyA5LjQwOTczIDEzLjkwOCA5LjIxNzk5QzEzLjc1MTYgOS4xMzgzIDEzLjUyNzQgOS4wNzMzNyAxMy4wODkgOS4wMzc1NUMxMi42Mzg5IDkuMDAwNzggMTIuMDU2NiA5IDExLjIgOUg3LjhDNi45NDM0MiA5IDYuMzYxMTMgOS4wMDA3OCA1LjkxMTA0IDkuMDM3NTVaIiAvPjwvc3ZnPg==)]{._4jUWi
.pdMy8}]{.block .relative .w-[var(--button-icon-size)]
.h-[var(--button-icon-size)] transition-position="absolute"
style="--tg-will-change: transform, opacity; --tg-enter-opacity: 1; --tg-enter-transform: scale(1); --tg-enter-filter: none; --tg-enter-duration: 300ms; --tg-enter-delay: 150ms; --tg-enter-timing-function: var(--cubic-enter); --tg-exit-opacity: 0; --tg-exit-transform: scale(0.6); --tg-exit-filter: none; --tg-exit-duration: 150ms; --tg-exit-delay: 0ms; --tg-exit-timing-function: var(--cubic-exit); --tg-initial-opacity: 0; --tg-initial-transform: scale(0.6); --tg-initial-filter: none;"}]{.NBPKZ}
::::::

:::::: {.code-sample-body .code-sample-body-small .code-sample-body-with-header}
::: {.code-block .hidden}
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-5",
    prompt: {
        id: "pmpt_abc123",
        version: "2",
        variables: {
            customer_name: "Jane Doe",
            product: "40oz juice box"
        }
    }
});

console.log(response.output_text);
```
:::

::: code-block
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    prompt={
        "id": "pmpt_abc123",
        "version": "2",
        "variables": {
            "customer_name": "Jane Doe",
            "product": "40oz juice box"
        }
    }
)

print(response.output_text)
```
:::

::: {.code-block .hidden}
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5",
    "prompt": {
      "id": "pmpt_abc123",
      "version": "2",
      "variables": {
        "customer_name": "Jane Doe",
        "product": "40oz juice box"
      }
    }
  }'
```
:::
::::::
:::::::::::

</div>

</div>

<div>

::: hidden
Variables with file input
:::

:::::::::::: hidden
::::::::::: {.code-sample .dark-mode}
:::::: code-sample-header
::: {.code-sample-title .body-small}
Prompt template with file input variable
:::

:::: exclude-from-copy
[[python]{.ktL9G}]{#select-trigger-:r1c: .fsluc role="button"
tabindex="0" variant="ghost" data-size="sm" data-selected="true"
aria-disabled="false" type="button" aria-haspopup="dialog"
aria-expanded="false" aria-controls="radix-:r1e:" state="closed"}

::: FJZOe
![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMWVtIiBoZWlnaHQ9IjFlbSIgdmlld2JveD0iMCAwIDEwIDE2IiBmaWxsPSJjdXJyZW50Q29sb3IiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgY2xhc3M9InlnenM2Ij48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTQuMzQxNTEgMC43NDc0MjNDNC43MTg1NCAwLjQxNzUyNiA1LjI4MTQ5IDAuNDE3NTI2IDUuNjU4NTIgMC43NDc0MjNMOS42NTg1MiA0LjI0NzQyQzEwLjA3NDIgNC42MTExMSAxMC4xMTYzIDUuMjQyODcgOS43NTI1OSA1LjY1ODVDOS4zODg5MSA2LjA3NDE0IDguNzU3MTUgNi4xMTYyNiA4LjM0MTUxIDUuNzUyNThMNS4wMDAwMSAyLjgyODc3TDEuNjU4NTIgNS43NTI1OEMxLjI0Mjg4IDYuMTE2MjYgMC42MTExMiA2LjA3NDE0IDAuMjQ3NDM4IDUuNjU4NUMtMC4xMTYyNDQgNS4yNDI4NyAtMC4wNzQxMjY3IDQuNjExMTEgMC4zNDE1MSA0LjI0NzQyTDQuMzQxNTEgMC43NDc0MjNaTTAuMjQ2MDY1IDEwLjM1NzhDMC42MDg4NzkgOS45NDEzOSAxLjI0MDU1IDkuODk3OTUgMS42NTY5NSAxMC4yNjA4TDUuMDAwMDEgMTMuMTczN0w4LjM0MzA4IDEwLjI2MDhDOC43NTk0OCA5Ljg5Nzk1IDkuMzkxMTUgOS45NDEzOSA5Ljc1Mzk2IDEwLjM1NzhDMTAuMTE2OCAxMC43NzQyIDEwLjA3MzMgMTEuNDA1OCA5LjY1Njk1IDExLjc2ODdMNS42NTY5NSAxNS4yNTM5QzUuMjgwNDMgMTUuNTgyIDQuNzE5NiAxNS41ODIgNC4zNDMwOCAxNS4yNTM5TDAuMzQzMDgyIDExLjc2ODdDLTAuMDczMzEyOCAxMS40MDU4IC0wLjExNjc0OSAxMC43NzQyIDAuMjQ2MDY1IDEwLjM1NzhaIiAvPjwvc3ZnPg==){.ygzs6}
:::
::::

[[[![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjFlbSIgaGVpZ2h0PSIxZW0iPjxwYXRoIGQ9Ik0xMi43NTg3IDJIMTYuMjQxM0MxNy4wNDYzIDEuOTk5OTkgMTcuNzEwNiAxLjk5OTk4IDE4LjI1MTggMi4wNDQxOUMxOC44MTM5IDIuMDkwMTIgMTkuMzMwNiAyLjE4ODY4IDE5LjgxNiAyLjQzNTk3QzIwLjU2ODYgMi44MTk0NyAyMS4xODA1IDMuNDMxMzkgMjEuNTY0IDQuMTg0MDRDMjEuODExMyA0LjY2OTM3IDIxLjkwOTkgNS4xODYwOCAyMS45NTU4IDUuNzQ4MTdDMjIgNi4yODkzNiAyMiA2Ljk1MzcyIDIyIDcuNzU4NjhWMTEuMjQxM0MyMiAxMi4wNDYzIDIyIDEyLjcxMDYgMjEuOTU1OCAxMy4yNTE4QzIxLjkwOTkgMTMuODEzOSAyMS44MTEzIDE0LjMzMDYgMjEuNTY0IDE0LjgxNkMyMS4xODA1IDE1LjU2ODYgMjAuNTY4NiAxNi4xODA1IDE5LjgxNiAxNi41NjRDMTkuMzMwNiAxNi44MTEzIDE4LjgxMzkgMTYuOTA5OSAxOC4yNTE4IDE2Ljk1NThDMTcuODkwNiAxNi45ODUzIDE3LjQ3NDUgMTYuOTk1MSAxNi45OTg0IDE2Ljk5ODRDMTYuOTk1MSAxNy40NzQ1IDE2Ljk4NTMgMTcuODkwNiAxNi45NTU4IDE4LjI1MThDMTYuOTA5OSAxOC44MTM5IDE2LjgxMTMgMTkuMzMwNiAxNi41NjQgMTkuODE2QzE2LjE4MDUgMjAuNTY4NiAxNS41Njg2IDIxLjE4MDUgMTQuODE2IDIxLjU2NEMxNC4zMzA2IDIxLjgxMTMgMTMuODEzOSAyMS45MDk5IDEzLjI1MTggMjEuOTU1OEMxMi43MTA2IDIyIDEyLjA0NjMgMjIgMTEuMjQxMyAyMkg3Ljc1ODY4QzYuOTUzNzIgMjIgNi4yODkzNiAyMiA1Ljc0ODE4IDIxLjk1NThDNS4xODYwOCAyMS45MDk5IDQuNjY5MzcgMjEuODExMyA0LjE4NDA0IDIxLjU2NEMzLjQzMTM5IDIxLjE4MDUgMi44MTk0NyAyMC41Njg2IDIuNDM1OTcgMTkuODE2QzIuMTg4NjggMTkuMzMwNiAyLjA5MDEyIDE4LjgxMzkgMi4wNDQxOSAxOC4yNTE4QzEuOTk5OTggMTcuNzEwNiAxLjk5OTk5IDE3LjA0NjMgMiAxNi4yNDEzVjEyLjc1ODdDMS45OTk5OSAxMS45NTM3IDEuOTk5OTggMTEuMjg5NCAyLjA0NDE5IDEwLjc0ODJDMi4wOTAxMiAxMC4xODYxIDIuMTg4NjggOS42NjkzNyAyLjQzNTk3IDkuMTg0MDRDMi44MTk0NyA4LjQzMTM5IDMuNDMxMzkgNy44MTk0NyA0LjE4NDA0IDcuNDM1OThDNC42NjkzNyA3LjE4ODY4IDUuMTg2MDggNy4wOTAxMiA1Ljc0ODE3IDcuMDQ0MTlDNi4xMDkzOSA3LjAxNDY4IDYuNTI1NDggNy4wMDQ4NyA3LjAwMTYyIDcuMDAxNjJDNy4wMDQ4NyA2LjUyNTQ4IDcuMDE0NjggNi4xMDkzOSA3LjA0NDE5IDUuNzQ4MTdDNy4wOTAxMiA1LjE4NjA4IDcuMTg4NjggNC42NjkzNyA3LjQzNTk4IDQuMTg0MDRDNy44MTk0NyAzLjQzMTM5IDguNDMxMzkgMi44MTk0NyA5LjE4NDA0IDIuNDM1OTdDOS42NjkzNyAyLjE4ODY4IDEwLjE4NjEgMi4wOTAxMiAxMC43NDgyIDIuMDQ0MTlDMTEuMjg5NCAxLjk5OTk4IDExLjk1MzcgMS45OTk5OSAxMi43NTg3IDJaTTkuMDAxNzYgN0wxMS4yNDEzIDdDMTIuMDQ2MyA2Ljk5OTk5IDEyLjcxMDYgNi45OTk5OCAxMy4yNTE4IDcuMDQ0MTlDMTMuODEzOSA3LjA5MDEyIDE0LjMzMDYgNy4xODg2OCAxNC44MTYgNy40MzU5OEMxNS41Njg2IDcuODE5NDcgMTYuMTgwNSA4LjQzMTM5IDE2LjU2NCA5LjE4NDA0QzE2LjgxMTMgOS42NjkzNyAxNi45MDk5IDEwLjE4NjEgMTYuOTU1OCAxMC43NDgyQzE3IDExLjI4OTQgMTcgMTEuOTUzNyAxNyAxMi43NTg3VjE0Ljk5ODJDMTcuNDQ1NSAxNC45OTUxIDE3Ljc5NTQgMTQuOTg2NCAxOC4wODkgMTQuOTYyNEMxOC41Mjc0IDE0LjkyNjYgMTguNzUxNiAxNC44NjE3IDE4LjkwOCAxNC43ODJDMTkuMjg0MyAxNC41OTAzIDE5LjU5MDMgMTQuMjg0MyAxOS43ODIgMTMuOTA4QzE5Ljg2MTcgMTMuNzUxNiAxOS45MjY2IDEzLjUyNzQgMTkuOTYyNCAxMy4wODlDMTkuOTk5MiAxMi42Mzg5IDIwIDEyLjA1NjYgMjAgMTEuMlY3LjhDMjAgNi45NDM0MiAxOS45OTkyIDYuMzYxMTMgMTkuOTYyNCA1LjkxMTA0QzE5LjkyNjYgNS40NzI2MiAxOS44NjE3IDUuMjQ4NDIgMTkuNzgyIDUuMDkyMDJDMTkuNTkwMyA0LjcxNTcgMTkuMjg0MyA0LjQwOTczIDE4LjkwOCA0LjIxNzk5QzE4Ljc1MTYgNC4xMzgzIDE4LjUyNzQgNC4wNzMzNyAxOC4wODkgNC4wMzc1NUMxNy42Mzg5IDQuMDAwNzggMTcuMDU2NiA0IDE2LjIgNEgxMi44QzExLjk0MzQgNCAxMS4zNjExIDQuMDAwNzggMTAuOTExIDQuMDM3NTVDMTAuNDcyNiA0LjA3MzM3IDEwLjI0ODQgNC4xMzgzIDEwLjA5MiA0LjIxNzk5QzkuNzE1NyA0LjQwOTczIDkuNDA5NzMgNC43MTU3IDkuMjE3OTkgNS4wOTIwMkM5LjEzODMgNS4yNDg0MiA5LjA3MzM3IDUuNDcyNjIgOS4wMzc1NSA1LjkxMTA0QzkuMDEzNTcgNi4yMDQ2MyA5LjAwNDg5IDYuNTU0NDcgOS4wMDE3NiA3Wk01LjkxMTA0IDkuMDM3NTVDNS40NzI2MiA5LjA3MzM3IDUuMjQ4NDIgOS4xMzgzIDUuMDkyMDIgOS4yMTc5OUM0LjcxNTcgOS40MDk3MyA0LjQwOTczIDkuNzE1NyA0LjIxNzk5IDEwLjA5MkM0LjEzODMgMTAuMjQ4NCA0LjA3MzM3IDEwLjQ3MjYgNC4wMzc1NSAxMC45MTFDNC4wMDA3OCAxMS4zNjExIDQgMTEuOTQzNCA0IDEyLjhWMTYuMkM0IDE3LjA1NjYgNC4wMDA3OCAxNy42Mzg5IDQuMDM3NTUgMTguMDg5QzQuMDczMzcgMTguNTI3NCA0LjEzODMgMTguNzUxNiA0LjIxNzk5IDE4LjkwOEM0LjQwOTczIDE5LjI4NDMgNC43MTU3IDE5LjU5MDMgNS4wOTIwMiAxOS43ODJDNS4yNDg0MiAxOS44NjE3IDUuNDcyNjIgMTkuOTI2NiA1LjkxMTA0IDE5Ljk2MjRDNi4zNjExMyAxOS45OTkyIDYuOTQzNDIgMjAgNy44IDIwSDExLjJDMTIuMDU2NiAyMCAxMi42Mzg5IDE5Ljk5OTIgMTMuMDg5IDE5Ljk2MjRDMTMuNTI3NCAxOS45MjY2IDEzLjc1MTYgMTkuODYxNyAxMy45MDggMTkuNzgyQzE0LjI4NDMgMTkuNTkwMyAxNC41OTAzIDE5LjI4NDMgMTQuNzgyIDE4LjkwOEMxNC44NjE3IDE4Ljc1MTYgMTQuOTI2NiAxOC41Mjc0IDE0Ljk2MjQgMTguMDg5QzE0Ljk5OTIgMTcuNjM4OSAxNSAxNy4wNTY2IDE1IDE2LjJWMTIuOEMxNSAxMS45NDM0IDE0Ljk5OTIgMTEuMzYxMSAxNC45NjI0IDEwLjkxMUMxNC45MjY2IDEwLjQ3MjYgMTQuODYxNyAxMC4yNDg0IDE0Ljc4MiAxMC4wOTJDMTQuNTkwMyA5LjcxNTcgMTQuMjg0MyA5LjQwOTczIDEzLjkwOCA5LjIxNzk5QzEzLjc1MTYgOS4xMzgzIDEzLjUyNzQgOS4wNzMzNyAxMy4wODkgOS4wMzc1NUMxMi42Mzg5IDkuMDAwNzggMTIuMDU2NiA5IDExLjIgOUg3LjhDNi45NDM0MiA5IDYuMzYxMTMgOS4wMDA3OCA1LjkxMTA0IDkuMDM3NTVaIiAvPjwvc3ZnPg==)]{._4jUWi
.pdMy8}]{.block .relative .w-[var(--button-icon-size)]
.h-[var(--button-icon-size)] transition-position="absolute"
style="--tg-will-change: transform, opacity; --tg-enter-opacity: 1; --tg-enter-transform: scale(1); --tg-enter-filter: none; --tg-enter-duration: 300ms; --tg-enter-delay: 150ms; --tg-enter-timing-function: var(--cubic-enter); --tg-exit-opacity: 0; --tg-exit-transform: scale(0.6); --tg-exit-filter: none; --tg-exit-duration: 150ms; --tg-exit-delay: 0ms; --tg-exit-timing-function: var(--cubic-exit); --tg-initial-opacity: 0; --tg-initial-transform: scale(0.6); --tg-initial-filter: none;"}]{.NBPKZ}
::::::

:::::: {.code-sample-body .code-sample-body-small .code-sample-body-with-header}
::: {.code-block .hidden}
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
import fs from "fs";
import OpenAI from "openai";
const client = new OpenAI();

// Upload a PDF we will reference in the prompt variables
const file = await client.files.create({
    file: fs.createReadStream("draconomicon.pdf"),
    purpose: "user_data",
});

const response = await client.responses.create({
    model: "gpt-5",
    prompt: {
        id: "pmpt_abc123",
        variables: {
            topic: "Dragons",
            reference_pdf: {
                type: "input_file",
                file_id: file.id,
            },
        },
    },
});

console.log(response.output_text);
```
:::

::: code-block
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
import openai, pathlib

client = openai.OpenAI()

# Upload a PDF we will reference in the variables
file = client.files.create(
    file=open("draconomicon.pdf", "rb"),
    purpose="user_data",
)

response = client.responses.create(
    model="gpt-5",
    prompt={
        "id": "pmpt_abc123",
        "variables": {
            "topic": "Dragons",
            "reference_pdf": {
                "type": "input_file",
                "file_id": file.id,
            },
        },
    },
)

print(response.output_text)
```
:::

::: {.code-block .hidden}
``` {.hljs .syntax-highlighter .dark-mode .code-sample-pre}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
# Assume you have already uploaded the PDF and obtained FILE_ID
curl https://api.openai.com/v1/responses   -H "Authorization: Bearer $OPENAI_API_KEY"   -H "Content-Type: application/json"   -d '{
    "model": "gpt-5",
    "prompt": {
      "id": "pmpt_abc123",
      "variables": {
        "topic": "Dragons",
        "reference_pdf": {
          "type": "input_file",
          "file_id": "file-abc123"
        }
      }
    }
  }'
```
:::
::::::
:::::::::::
::::::::::::

</div>
::::::::::::::::::::::::::::::

::: anchor-heading-wrapper
## Next steps![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjE1IiBoZWlnaHQ9IjE1IiBjbGFzcz0iYW5jaG9yLWhlYWRpbmctaWNvbiIgcm9sZT0icHJlc2VudGF0aW9uIj48cGF0aCBkPSJNMTguMjkyOSA1LjcwNzFDMTYuNDc0MyAzLjg4ODQ5IDEzLjUyNTcgMy44ODg0OSAxMS43MDcxIDUuNzA3MUwxMC43MDcxIDYuNzA3MUMxMC4zMTY2IDcuMDk3NjMgOS42ODM0MSA3LjA5NzYzIDkuMjkyODkgNi43MDcxQzguOTAyMzYgNi4zMTY1OCA4LjkwMjM2IDUuNjgzNDEgOS4yOTI4OSA1LjI5Mjg5TDEwLjI5MjkgNC4yOTI4OUMxMi44OTI2IDEuNjkzMjIgMTcuMTA3NCAxLjY5MzIyIDE5LjcwNzEgNC4yOTI4OUMyMi4zMDY4IDYuODkyNTUgMjIuMzA2OCAxMS4xMDc0IDE5LjcwNzEgMTMuNzA3MUwxOC43MDcxIDE0LjcwNzFDMTguMzE2NiAxNS4wOTc2IDE3LjY4MzQgMTUuMDk3NiAxNy4yOTI5IDE0LjcwNzFDMTYuOTAyNCAxNC4zMTY2IDE2LjkwMjQgMTMuNjgzNCAxNy4yOTI5IDEzLjI5MjlMMTguMjkyOSAxMi4yOTI5QzIwLjExMTUgMTAuNDc0MyAyMC4xMTE1IDcuNTI1NzIgMTguMjkyOSA1LjcwNzFaTTE1LjcwNzEgOC4yOTI4OUMxNi4wOTc2IDguNjgzNDEgMTYuMDk3NiA5LjMxNjU4IDE1LjcwNzEgOS43MDcxTDkuNzA3MSAxNS43MDcxQzkuMzE2NTggMTYuMDk3NiA4LjY4MzQxIDE2LjA5NzYgOC4yOTI4OSAxNS43MDcxQzcuOTAyMzYgMTUuMzE2NiA3LjkwMjM2IDE0LjY4MzQgOC4yOTI4OSAxNC4yOTI5TDE0LjI5MjkgOC4yOTI4OUMxNC42ODM0IDcuOTAyMzYgMTUuMzE2NiA3LjkwMjM2IDE1LjcwNzEgOC4yOTI4OVpNNi43MDcxIDkuMjkyODlDNy4wOTc2MyA5LjY4MzQxIDcuMDk3NjMgMTAuMzE2NiA2LjcwNzEgMTAuNzA3MUw1LjcwNzEgMTEuNzA3MUMzLjg4ODQ5IDEzLjUyNTcgMy44ODg0OSAxNi40NzQzIDUuNzA3MSAxOC4yOTI5QzcuNTI1NzIgMjAuMTExNSAxMC40NzQzIDIwLjExMTUgMTIuMjkyOSAxOC4yOTI5TDEzLjI5MjkgMTcuMjkyOUMxMy42ODM0IDE2LjkwMjQgMTQuMzE2NiAxNi45MDI0IDE0LjcwNzEgMTcuMjkyOUMxNS4wOTc2IDE3LjY4MzQgMTUuMDk3NiAxOC4zMTY2IDE0LjcwNzEgMTguNzA3MUwxMy43MDcxIDE5LjcwNzFDMTEuMTA3NCAyMi4zMDY4IDYuODkyNTUgMjIuMzA2OCA0LjI5Mjg5IDE5LjcwNzFDMS42OTMyMiAxNy4xMDc0IDEuNjkzMjIgMTIuODkyNiA0LjI5Mjg5IDEwLjI5MjlMNS4yOTI4OSA5LjI5Mjg5QzUuNjgzNDEgOC45MDIzNiA2LjMxNjU4IDguOTAyMzYgNi43MDcxIDkuMjkyODlaIiAvPjwvc3ZnPg==){.anchor-heading-icon} {#next-steps .anchor-heading data-name="next-steps"}
:::

Now that you known the basics of text inputs and outputs, you might want
to check out one of these resources next.

[](/chat/edit)

::::::::: {.icon-item .mt-2}
::: icon-item-icon
![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxZW0iIGhlaWdodD0iMWVtIiBmaWxsPSJjdXJyZW50Q29sb3IiIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMTUuMjQgMy40ODZ2LjAwMmwtMS4wNTYgNC41MTdoNS44MjNjMS43MjYgMCAyLjU5NiAyLjAyMSAxLjUxOCAzLjNsLS4wMDIuMDAzLTkuMzA4IDEwLjk2NS0uMDAyLjAwMmMtMS4zOTcgMS42NTYtMy45MjIuMjIzLTMuNDU0LTEuNzZ2LS4wMDNsMS4wNTctNC41MTdIMy45OTNjLTEuNzI2IDAtMi41OTYtMi4wMjEtMS41MTktMy4zbC4wMDMtLjAwMyA5LjMwOC0xMC45NjUuMDAyLS4wMDJjMS4zOTctMS42NTYgMy45MjItLjIyMyAzLjQ1NCAxLjc2Wm0tMS45NS0uNDQ0LTEuMzQgNS43MzVhLjk5OC45OTggMCAwIDAgLjk3MyAxLjIyNmg3LjA3NGEuMDQuMDQgMCAwIDEgLjAwMy4wMS4wNDUuMDQ1IDAgMCAxLS4wMDQuMDA1bC05LjI4NyAxMC45NCAxLjM0MS01LjczNWEuOTk4Ljk5OCAwIDAgMC0uOTczLTEuMjI2SDQuMDAzYS4wNDEuMDQxIDAgMCAxLS4wMDMtLjAxbC4wMDQtLjAwNSA5LjI4Ny0xMC45NFoiIGNsaXAtcnVsZT0iZXZlbm9kZCIgLz48L3N2Zz4=)
:::

::::::: icon-item-right
::::: icon-item-title
::: {.icon-item-title .body-large}
Build a prompt in the Playground
:::

::: pointer
![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgZmlsbD0iY3VycmVudENvbG9yIiB2aWV3Ym94PSIwIDAgMjQgMjQiPjxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgZD0iTTkuMjkzIDcuMjkzYTEgMSAwIDAgMSAxLjQxNCAwbDQgNGExIDEgMCAwIDEgMCAxLjQxNGwtNCA0YTEgMSAwIDAgMS0xLjQxNC0xLjQxNEwxMi41ODYgMTIgOS4yOTMgOC43MDdhMSAxIDAgMCAxIDAtMS40MTRaIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIC8+PC9zdmc+)
:::
:::::

::: {.icon-item-desc .body-small}
Use the Playground to develop and iterate on prompts.
:::
:::::::
:::::::::

[](/docs/guides/structured-outputs)

::::::::: {.icon-item .mt-2}
::: icon-item-icon
![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxZW0iIGhlaWdodD0iMWVtIiBmaWxsPSJjdXJyZW50Q29sb3IiIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMTIuNSAzLjQ0NGExIDEgMCAwIDAtMSAwbC02LjI1MyAzLjYxIDYuNzY4IDMuODA3IDYuOTU1LTMuNjgyLTYuNDctMy43MzVabTcuMTYgNS42MzJMMTMgMTIuNjAydjcuNjY2bDYuMTYtMy41NTZhMSAxIDAgMCAwIC41LS44NjdWOS4wNzZaTTExIDIwLjI2OHYtNy42ODNMNC4zNCA4LjgzOXY3LjAwNmExIDEgMCAwIDAgLjUuODY3TDExIDIwLjI2OFptLS41LTE4LjU1N2EzIDMgMCAwIDEgMyAwbDYuNjYgMy44NDZhMyAzIDAgMCAxIDEuNSAyLjU5OHY3LjY5YTMgMyAwIDAgMS0xLjUgMi41OThMMTMuNSAyMi4yOWEzIDMgMCAwIDEtMyAwbC02LjY2LTMuODQ2YTMgMyAwIDAgMS0xLjUtMi41OTh2LTcuNjlhMyAzIDAgMCAxIDEuNS0yLjU5OEwxMC41IDEuNzFaIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIC8+PC9zdmc+)
:::

::::::: icon-item-right
::::: icon-item-title
::: {.icon-item-title .body-large}
Generate JSON data with Structured Outputs
:::

::: pointer
![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgZmlsbD0iY3VycmVudENvbG9yIiB2aWV3Ym94PSIwIDAgMjQgMjQiPjxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgZD0iTTkuMjkzIDcuMjkzYTEgMSAwIDAgMSAxLjQxNCAwbDQgNGExIDEgMCAwIDEgMCAxLjQxNGwtNCA0YTEgMSAwIDAgMS0xLjQxNC0xLjQxNEwxMi41ODYgMTIgOS4yOTMgOC43MDdhMSAxIDAgMCAxIDAtMS40MTRaIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIC8+PC9zdmc+)
:::
:::::

::: {.icon-item-desc .body-small}
Ensure JSON data emitted from a model conforms to a JSON schema.
:::
:::::::
:::::::::

[](/docs/api-reference/responses)

::::::::: {.icon-item .mt-2}
::: icon-item-icon
![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxZW0iIGhlaWdodD0iMWVtIiBmaWxsPSJjdXJyZW50Q29sb3IiIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMTQuNDQ3IDcuMTA2YTEgMSAwIDAgMSAuNDQ3IDEuMzQxbC00IDhhMSAxIDAgMSAxLTEuNzg4LS44OTRsNC04YTEgMSAwIDAgMSAxLjM0MS0uNDQ3Wk02LjYgNy4yYTEgMSAwIDAgMSAuMiAxLjRMNC4yNSAxMmwyLjU1IDMuNGExIDEgMCAwIDEtMS42IDEuMmwtMy00YTEgMSAwIDAgMSAwLTEuMmwzLTRhMSAxIDAgMCAxIDEuNC0uMlptMTAuOCAwYTEgMSAwIDAgMSAxLjQuMmwzIDRhMSAxIDAgMCAxIDAgMS4ybC0zIDRhMSAxIDAgMCAxLTEuNi0xLjJsMi41NS0zLjQtMi41NS0zLjRhMSAxIDAgMCAxIC4yLTEuNFoiIGNsaXAtcnVsZT0iZXZlbm9kZCIgLz48L3N2Zz4=)
:::

::::::: icon-item-right
::::: icon-item-title
::: {.icon-item-title .body-large}
Full API reference
:::

::: pointer
![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgZmlsbD0iY3VycmVudENvbG9yIiB2aWV3Ym94PSIwIDAgMjQgMjQiPjxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgZD0iTTkuMjkzIDcuMjkzYTEgMSAwIDAgMSAxLjQxNCAwbDQgNGExIDEgMCAwIDEgMCAxLjQxNGwtNCA0YTEgMSAwIDAgMS0xLjQxNC0xLjQxNEwxMi41ODYgMTIgOS4yOTMgOC43MDdhMSAxIDAgMCAxIDAtMS40MTRaIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIC8+PC9zdmc+)
:::
:::::

::: {.icon-item-desc .body-small}
Check out all the options for text generation in the API reference.
:::
:::::::
:::::::::

</div>
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:::::: S7rz6
::::: jXvCY
:::: -nkvM
::: {.LaMoi style="--active-track-top: 119px; --active-track-height: 24px;"}
:::
::::

- [[Text input and output]{.OjNLJ aria-hidden="true"}Text input and
  output](#page-top){.kbmsS active="false"}
- [[Prompt engineering]{.OjNLJ aria-hidden="true"}Prompt
  engineering](#prompt-engineering){.kbmsS active="false"}
- [[Message roles and instruction following]{.OjNLJ
  aria-hidden="true"}Message roles and instruction
  following](#message-roles-and-instruction-following){.kbmsS
  active="false"}
- [[Reusable prompts]{.OjNLJ aria-hidden="true"}Reusable
  prompts](#reusable-prompts){.kbmsS active="true"}
- [[Next steps]{.OjNLJ aria-hidden="true"}Next
  steps](#next-steps){.kbmsS active="false"}
:::::
::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
