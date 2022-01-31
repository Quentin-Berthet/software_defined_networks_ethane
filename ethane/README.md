# Résumé

## Partie 1
L'architecture réseau Ethane vise en particulier les entreprises car elles ont besoin d'avoir un réseau facilement gérable, securisé et disponible. Ehtane propose 3 principes fondamentaux :
* Le réseau devrait être régi par des politiques déclarées sur des noms de haut niveau
  * il faut déclarer les services qu'un utilisateur peut accéder et avec quelle machine, sans utiliser les adresse IPs
* La politique devrait déterminer le chemin que suivent les paquets
  * le gestionnaire de réseau doit pouvoir déterminer le meilleur chemins pour un service donné selon la politique qu'il souhaite
* Le réseau devrait imposer un lien fort entre un paquet et son origine
    * les adresses IPs sont dynamiques et donc il est très facile de spoofer l'origine d'un paquet, cela pose un problème de sécurité

## Partie 2
Ethane autorise par défaut, aucune communication entre deux machines. Il y a deux composants principaux
* un *Controller* central qui contient la politique de sécurité du réseau global
* des Ethane *Swiches*, qui s'occupe de forwarder les paquets s'ils respectent la politique de sécurité. En d'autres termes, quand un paquet arrive, il est transmis au *Controller* pour vérifier que celui-ci peut être transmis.
Le fonctionnement d'Ethan se fait via 5 étapes :
1. l'enregistrement, tout les *switchs*, utilisateurs, hôtes sont enregistrés dans le *Controller* via l'adresse MAC ou pseudo/mdp, ou via des certificats.
2. *bootstraping*, un spanning tree est construit avec comme noeud racine le *Controller*.
3. authentification
4. *Flow setup*
5. *Forwarding*

## Partie 4
Le langage Pol-Eth permet de définir les règles de politique de sécurité réseau. Le langage est relativement simple, il suffit de définir une condition à vérifier et l'action à effectuer si la condition est vraie. Les règles écritent en début de fichier sont les plus importantes. Le langage Pol-Eth est un langage compié avec des fonctions de recherches JIT. Le fichier de configuration est converti en C++ et compilé.

## Partie 5
Pour effectuer des tests, ils ont prototypé 3 types de *switchs* :
1. *Ethane 4-port Gigabit Ethernet Switch*, implémenté sur une carte FPGA,
2. *Ethane 4-port Gigabit Ethernet Switch*, implémenté via un ordinateur de bureau
3. *Ethane Wireless Access Point*, implémenté via l'utilisation d'un routeur Linksys + OpenWRT.
Le *switch* matériel est beaucoup plus performant car il peut gérer les paquets à une vitesse de 1Gb/s, alors que le *switch* logiciel peut seulement atteindre cette vitesse si le paquet fait la taille MTU. En dessous, la vitesse baisse à 16 Mb/s. Le *wireless access point* a une vitesse de 23 Mb/s.
Le *controller* a été implémenté via l'utilisation d'un ordinateur classique tourant sur GNU/Linux et l'authentification des utilisateurs se fait via Kerberos.
Ainsi, 19 switchs ont été déployé avec 300 hôtes enregistrés et 120 hôtes actif sur une moyenne de 5 minutes, le tout sur un réseau de 100 Mb/s.
## Partie 7
Plusieurs problèmes ont été rencontrés :
* Ethane supprime le système de VLAN qui est utilisé pour contrôler le broadcast (ARP, OSPF, ...) ce qui engendre un très grand nombre de message dans le réseau et peut provoquer des problèmes de sécurité notamment pour ARP. Le seul moyen de régler ce problème et de créer une norme pour enregistrer les services.
* si A peut parler avec B (vice-versa) mais pas avec C et que B peut parler avec C (vice versa), alors A peut parler indirectement avec C grâce à B qui va rediriger le message à C. Le problème nécessite de modifier l'OS.
* Ethane assume que le port utilisé est pour la bonne application (port 80, HTTP), mais il est possible d'utiliser ces ports pour d'autres applications via un tunnel. Le problème peut être réglé avec un proxy application.
* une personne peut spoofer son adresse MAC mais il est possible d'éviter ce problème en utilisatn la norme 802.1X + AE.
## Partie 8
Ethane a pour but de simplifier le *data-plane* et de centraliser le *control-plane*. Il est plus nécessaire de faire des VLANs ce qui facilite la gestion du réseau.
## Partie 9
Il est très facile et rapide de gérer un réseau Ethane notamment l'ajout d'un *switch*, utilisateur, règle de sécurité. La journalisation des logs permet de trouver facilement les erreurs réseaux et de les résoudre. Il est préférable de laisser les switchs faire le moins de tâches administrative possibles et de développer le *controller* (redondance, meilleurs performances).
