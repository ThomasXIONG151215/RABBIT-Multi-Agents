<div align="center">
<div align="center">
 <img alt="ASTRA" height="auto" src="../../images/cover2.png">
</div>

<a href="../../README.md"><img alt="README in English" src="https://img.shields.io/badge/English-lightgrey"></a>
<a href=".README-CN.md"><img alt="简体中文" src="https://img.shields.io/badge/简体中文-lightgrey"></a>
<a href=".README-FR.md"><img alt="Français" src="https://img.shields.io/badge/Français-lightgrey"></a>

<a href="">
<span>Exploitation Automatisée des Usines de Plantes</span>
</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="">
<span>Opération Collaborative Multi-Agent</span>
</a>
</div>

* **Vision** : En exploitant la technologie des usines de plantes, nous visons à garantir que les gens ne dépendent plus des conditions météorologiques pour se nourrir, permettant un accès toute l'année à des fruits et légumes sans pollution et sans pesticides partout, y compris dans l'espace.

* **Défi** : Bien que les usines de plantes puissent collecter de nombreuses données basées sur la technologie IoT, l'analyse et le traitement de ces données nécessitent encore une implication significative des ingénieurs, avec de nombreuses tâches étant très répétitives.

* **Solution** : Grâce à un flux de travail automatisé Multi-Agent piloté par des modèles de langage larges (LLM), nous déployons trois agents IA :

    * Analyste de Données IA : Utilise le modèle qwen-max pour analyser les données historiques et fournir les résultats à l'Agronome Assistant IA.
    * Agronome Assistant IA : Combine les documents RAG et les résultats de l'Analyste de Données IA pour offrir des recommandations de plantation, en utilisant le modèle moonshot-v1-128k pour le traitement de longs textes.
    * Ingénieur d'Exécution IA : Collabore avec des ingénieurs humains pour ajuster les paramètres des équipements de l'usine de plantes en fonction des résultats d'analyse.

<div align="center">
<img  alt="Visualisation Intelligente des Usines de Plantes" src="../../images/gif_data.gif">
</div>

# Approche Technique

Ce projet vise à tester les capacités du LLM dans :
1. Le traitement et l'analyse de longs textes et données : Évaluer sa compréhension mathématique et son utilisation des outils.
2. La conversion de textes en stratégies de plantation exploitables : Évaluer comment il extrait des documents professionnels pertinents de la base de connaissances et fournit des conseils scientifiques.
3. La conversion des stratégies en paramètres de contrôle des dispositifs réels : Déterminer si le LLM peut générer des valeurs spécifiques pour contrôler les équipements en fonction des stratégies de plantation.

# Structure du Flux de Travail

Les trois points de test sont représentés par trois Agents IA interconnectés. Nous évitons d'utiliser un Agent complet pour assurer que la portée de génération de texte du LLM reste contrôlable, chaque Agent traitant une tâche spécifique.

1. **Analyste de Données IA** : Analyse les données historiques, résume les conditions de différents paramètres de plantation et envoie les résultats de l'analyse à l'Agronome Assistant IA. Ici, le modèle qwen-max est utilisé pour analyser les dataframes pandas.

<div align="center">
<img  alt="Analyste de Données IA" src="../../images/gif_ai_analyst.gif">
</div>

2. **Agronome Assistant IA** : Traite les problèmes que les ingénieurs humains veulent résoudre en réduisant d'abord la portée des documents RAG à l'aide d'étiquettes, en extrayant des connaissances des documents sélectionnés et en fournissant une analyse préliminaire et des recommandations pour la prochaine étape de plantation. Pour gérer une grande quantité de contenu, le modèle moonshot-v1-128k est utilisé pour la mise en cache de longs textes.
<div align="center">
<img  alt="Agronome Assistant IA" src="../../images/gif_ai_expert.gif">
</div>

3. **Ingénieur d'Exécution IA** : Met à jour et détermine les conditions de croissance optimales des plantes sur la base de l'analyse cumulative. Après approbation par les ingénieurs humains, il exécute les ajustements et le contrôle des paramètres des équipements de l'usine de plantes.

<div align="center">
<img  alt="Ingénieur d'Exécution IA" src="../../images/gif_ai_engineer.gif">
</div>

**Exploiter les Points Forts et Éviter les Points Faibles** : Grâce au flux de travail ci-dessus, nous libérons les ingénieurs humains pour qu'ils se concentrent sur la prise de décision. En utilisant un flux de gestion de plantation multi-agent professionnel, nous exploitons les capacités de traitement et de résumé des longs textes du LLM et utilisons la technologie RAG avec des règles personnalisées et la mise en cache contextuelle de Moonshot pour atténuer les hallucinations du LLM.

<div align="center">
<img  alt="Panneau de Contrôle des Dispositifs" src="../../images/gif_device_control.gif">
</div>

# Nouveaux Outils Appris Lors du Lancement du Projet AdventureX

**Modèles LLM**

* Mise en cache de longs textes Moonshot
* Analyse statistique Tongyi Qianwen

**Récupération RAG**

* [Original] RAG à Portée Contrôlable Orienté Résolution de Problèmes

**Frontend & Déploiement**

* Zeabur
* Gamma

**Conception 2D**
- Midjourney
- Light Year AI

**Conception 3D**
- Tripo AI
- HyperHuman
