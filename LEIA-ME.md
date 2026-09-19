# Site do publisher — Sug's LowPoly

Site estático, em inglês, feito para servir de "Website" e "Customer Support" no perfil de publisher da Unity Asset Store. Tem página inicial, página do pack Low Poly Enemy Melee Weapons (galeria, conteúdo, especificações e FAQ), página de contato dedicada, página de privacidade e página 404. Não depende de nenhum serviço externo: fontes e imagens ficam na própria pasta, não há cookies, rastreadores nem formulários.

## O que tem nesta pasta

| Caminho | Para que serve |
|---|---|
| `docs/` | O site pronto. É esta pasta que o GitHub Pages publica |
| `site.json` | As quatro informações que mudam: e-mail, endereço do site e links da loja |
| `build.py` | Gera `docs/` de novo a partir de `src/` (só precisa de Python 3) |
| `src/` | Páginas, estilos, script, fontes e imagens de origem |
| `brand/` | Logo em SVG e PNG, favicon e a imagem de perfil do publisher |

## Antes de colocar no ar

Abra `site.json` e preencha:

```json
{
  "publisher": "Sug's LowPoly",
  "support_email": "seu-email-de-suporte@exemplo.com",
  "site_url": "https://guauglop.github.io/SugsLowPoly/",
  "pack_store_url": "",
  "publisher_store_url": ""
}
```

`support_email` é obrigatório: enquanto estiver vazio o site é gerado como rascunho, com um aviso no lugar do e-mail e com instrução para os buscadores não indexarem. `site_url` é o endereço final, com barra no fim; com ele o site ganha link canônico, imagem de compartilhamento e `sitemap.xml`. Os dois links da loja ficam vazios por enquanto. Quando o pack for aprovado, cole o link dele em `pack_store_url` e o selo "Coming soon" vira "Available now", com botão para a loja.

Depois rode, dentro desta pasta:

```
python build.py
```

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

Três trechos falam em seu nome e convém conferir: o parágrafo "How the packs are made" na página inicial e a última pergunta do FAQ, que declaram o uso de IA no mesmo sentido da página da loja; a página `privacy.html`, que promete não usar o e-mail de quem escreve para mais nada e apagar a conversa se a pessoa pedir; e a frase da página de contato que diz que as respostas costumam sair em alguns dias úteis, em inglês ou português. Tudo isso fica em `src/pages/`.

## Licenças

As fontes Anton, Barlow e Barlow Condensed são distribuídas sob a SIL Open Font License, que permite uso comercial e hospedagem própria; os textos das licenças estão em `src/assets/fonts`. As imagens são renders do próprio pack.
