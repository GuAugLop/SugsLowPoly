# Site do publisher — Sug's LowPoly

Site estático, em inglês, feito para servir de "Website" e "Customer Support" no perfil de publisher da Unity Asset Store. Tem página inicial com um card por pack, uma página para cada pack (Low Poly Enemy Melee Weapons e Low Poly Enemy Encampment Props: galeria, conteúdo, especificações, FAQ e um link cruzado "Pairs well with" entre as duas), página de contato dedicada, página de privacidade e página 404. Não depende de nenhum serviço externo: fontes e imagens ficam na própria pasta, não há cookies, rastreadores nem formulários.

## O que tem nesta pasta

| Caminho | Para que serve |
|---|---|
| `docs/` | O site pronto. É esta pasta que o GitHub Pages publica |
| `site.json` | As informações que mudam: e-mail, endereço do site e links da loja de cada pack |
| `build.py` | Gera `docs/` de novo a partir de `src/` (só precisa de Python 3) |
| `src/` | Páginas, estilos, script, fontes e imagens de origem |
| `src/data/packs/` | Um arquivo JSON por pack, com textos, galeria, especificações, FAQ e card |
| `src/templates/pack.html` | O modelo comum de onde saem todas as páginas de pack |
| `brand/` | Logo em SVG e PNG, favicon e a imagem de perfil do publisher |

## Antes de colocar no ar

Abra `site.json` e preencha:

```json
{
  "publisher": "Sug's LowPoly",
  "support_email": "seu-email-de-suporte@exemplo.com",
  "site_url": "https://guauglop.github.io/SugsLowPoly/",
  "pack_store_url": "",
  "store_urls": {
    "low-poly-enemy-melee-weapons": "",
    "low-poly-enemy-encampment-props": ""
  },
  "publisher_store_url": ""
}
```

`support_email` é obrigatório: enquanto estiver vazio o site é gerado como rascunho, com um aviso no lugar do e-mail e com instrução para os buscadores não indexarem. `site_url` é o endereço final, com barra no fim; com ele o site ganha link canônico, imagem de compartilhamento e `sitemap.xml`. Os links da loja ficam vazios por enquanto. Quando um pack for aprovado, cole o link dele em `store_urls`, na linha com o nome (slug) do pack, e rode o build: o selo "Coming soon" vira "Available", com botão para a loja, na página do pack, no card da página inicial e no card "Pairs well with" da outra página. O campo antigo `pack_store_url` continua valendo para o pack de armas quando a linha dele em `store_urls` está vazia; basta usar um dos dois.

Depois rode, dentro desta pasta:

```
python build.py
```

## Links da loja de cada pack

| Pack | Página | Onde colar o link | Link depois da aprovação |
|---|---|---|---|
| Low Poly Enemy Melee Weapons (pacote 409356) | `low-poly-enemy-melee-weapons.html` | `store_urls` → `low-poly-enemy-melee-weapons` (ou `pack_store_url`) | https://assetstore.unity.com/packages/slug/409356 (curto: https://u3d.as/4bsg) |
| Low Poly Enemy Encampment Props (pacote 410366) | `low-poly-enemy-encampment-props.html` | `store_urls` → `low-poly-enemy-encampment-props` | https://assetstore.unity.com/packages/slug/410366 (curto: https://u3d.as/4bTo) |

Cole o link só depois que o pack estiver publicado; antes disso ele não abre para o público. Depois de publicar os dois, também vale preencher `publisher_store_url` com a página do publisher na loja.

## Como adicionar um pack

1. Copie um dos arquivos de `src/data/packs/` para `src/data/packs/<slug>.json`. O nome do arquivo é o slug, que vira também o nome da página (`<slug>.html`). O campo `order` define a ordem na página inicial e nos menus.
2. Troque os textos. Campos que terminam em `_html`, as listas de parágrafos e de itens, os valores das especificações e as respostas do FAQ são HTML; os outros são texto simples. `nav_label` é o nome curto no menu do topo (precisa ser curto para caber em telas de 761 px). `pairs_with` é opcional e cria a seção "Pairs well with" com o card de outro pack.
3. Ponha as imagens em `src/assets/img/<pasta-do-pack>/`: `gallery/NN-nome.webp` com 1800 × 1200 e `gallery/NN-nome-thumb.webp` com 720 × 480 (WebP qualidade 82), `pack-card-1200.webp` (1200 × 800), `pack-banner-2000.webp` (2000 × 1050) e `pack-banner-1100.webp` (1100 × 578), e `og-image.jpg` (1200 × 630). Aponte o bloco `images` do JSON para elas.
4. O banner do topo da página vem do CSS, porque a política de segurança do site não aceita estilo dentro do HTML: copie as duas regras `art-encampment` do fim de `src/assets/css/site.css`, troque o nome e os caminhos e ponha o nome da classe em `images.banner_class`.
5. Acrescente `"<slug>": ""` em `store_urls` no `site.json` e rode `python build.py`. A página, o card da página inicial, os links do topo e do rodapé e o `sitemap.xml` saem sozinhos; o build para com uma mensagem se faltar alguma imagem. Revise à mão o texto da seção de packs da página inicial ("Two packs so far"), que é fixo.

## Publicar no GitHub Pages

Esta pasta é o repositório `GuAugLop/SugsLowPoly`. O GitHub Pages só publica a raiz ou a pasta `/docs` de uma branch, por isso o site pronto fica em `docs/`. A ativação é feita uma vez, no site do GitHub: **Settings → Pages → Build and deployment**, origem **Deploy from a branch**, branch `main`, pasta `/docs`, **Save**. Em um ou dois minutos o site abre em `https://guauglop.github.io/SugsLowPoly/`.

Para atualizar depois de qualquer mudança:

```
python build.py
git add -A
git commit -m "Update site"
git push
```

### Domínio próprio

O GitHub Pages aceita domínio próprio de graça, com HTTPS automático. A ordem recomendada pelo GitHub é: primeiro informar o domínio em **Settings → Pages → Custom domain**, depois criar os registros no DNS. Para o domínio raiz são quatro registros A (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`); para `www`, um CNAME apontando para `guauglop.github.io`. Com os dois configurados o GitHub redireciona um para o outro sozinho. A propagação e o certificado podem levar até 24 horas; quando a opção aparecer, marque **Enforce HTTPS**. Vale também verificar o domínio na conta (Settings da conta → Pages → Add a domain), o que impede que outra pessoa o use.

Depois troque o `site_url` do `site.json` para o endereço novo, por exemplo `https://www.seudominio.com/`, e gere o site de novo. Com um endereço que não termina em `github.io`, o `build.py` grava sozinho o arquivo `docs/CNAME`, que é onde o GitHub guarda o domínio; sem isso, cada build apagaria a configuração.

O `.gitignore` deixa de fora caches do Python, arquivos do Windows e de editores, e a pasta antiga `site/`, que era a saída do build antes de mudar para `docs/` e pode ser apagada. Se um dia o site for para um domínio próprio ou outra hospedagem, basta trocar o `site_url` e publicar o conteúdo de `docs/`.

## O que preencher no perfil de publisher da Unity

| Campo do perfil | O que usar |
|---|---|
| Profile picture | `brand/publisher-profile-1024.png` |
| Profile name | Sug's LowPoly |
| Website | O endereço do site (`site_url`) |
| Customer support, link | O endereço do site seguido de `contact.html` |
| Customer support, e-mail | O mesmo e-mail do `site.json` |

## Textos que valem a sua leitura

Três trechos falam em seu nome e convém conferir: o parágrafo "How the packs are made" na página inicial e a última pergunta do FAQ de cada pack, que declaram o uso de IA no mesmo sentido da página da loja (os textos dos packs ficam em `src/data/packs/`); a página `privacy.html`, que promete não usar o e-mail de quem escreve para mais nada e apagar a conversa se a pessoa pedir; e a frase da página de contato que diz que as respostas costumam sair em alguns dias úteis, em inglês ou português. As páginas fixas ficam em `src/pages/`.

## Licenças

As fontes Anton, Barlow e Barlow Condensed são distribuídas sob a SIL Open Font License, que permite uso comercial e hospedagem própria; os textos das licenças estão em `src/assets/fonts`. As imagens são renders dos próprios packs; o manequim e o cenário que aparecem em algumas delas são só demonstração, e as páginas dizem isso.
