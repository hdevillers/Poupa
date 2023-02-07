# PouPâ
Est une application de compilation de données de pousse de pâton. Elle doit être utilisé avec les dispositifs PouPâ.

## Quelques mots sur le projet
Afin de mieux comprendre la pousse du levain et l’influence de certains facteurs sur celle-ci, Frédéric Mabille et Denis Cassan ont conçu un dispositif expérimental, le « PouPâ » qui enregistre la pousse d’un pâton. Pour cela, le PouPâ est équipé d’un Arduino et de cinq capteurs, quatre capteurs de distance infrarouges et un capteur de température. Les pâtons sont placés dans des flacons et un piston est entrainé par la pousse de la pâte, c’est ce mouvement qui est enregistré par les capteurs infrarouges. <br></br>
Les utilisateurs de ce dispositif, chercheurs et boulangers, veulent pouvoir analyser et comparer les données obtenues. Pour cela, un code, sans interface utilisateur, avait été réalisé par un chercheur. Ce programme lisait, traitait et illustrait sous forme de graphiques les données des résultats stockés dans des fichiers. Celui-ci nécessitait de rentrer le nom du fichier de données directement dans le code python puis exécuter ce dernier, procédure irréalisable dans le cadre d’un outil participatif pour des non informaticiens. De plus, une volonté de facilité le partage des résultats entre chercheur et boulangers a été émise. Avec toutes ces contraintes, il existait donc un besoin de créer un outil accessible, en ligne et multi-plateforme pour permettre l’analyse de ses données. Ce projet a été réalisé en collaboration avec des chercheurs de l’unité SPO qui vont utiliser l’application lors d’expérimentation.
## Quelques mots sur l'outil utilisé et l'oragnisation du code
Ici, le framework Phython <a href=https://streamlit.io/>Streamlit</a> a été utilisé. Cependant, au moment de la création de l'application, il n'était pas possible de faire une application multipages nativement dans Streamlit. L'extention <a href=https://github.com/TangleSpace/hydralit>Hydralit</a> a été utilisé.
<br></br>
Dans *poupa_app.py*, retrouvez la création et la redirection de chacune des pages, un peu comme dans un routeur.
Vous retrouverez dans le dossier **app_pages** le code front de chacune des pages de l'application.
Le fichier *models.py* gère les interactions avec la base de données et le traitement des données (par exemple la génération des graphiques)
