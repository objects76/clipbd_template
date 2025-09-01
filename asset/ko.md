
# 초보자를 위한 워드 임베딩 설명

## 왜 AI는 언어를 이해하기 위해 수학이 필요한가?

[<img src='https://miro.medium.com/v2/resize:fill:64:64/1*CxjLF3hov8jOaHyzKZej5w.jpeg' alt='Felix Pappe' title='' width='32' height='32' />](/@felix-pappe?source=post_page---byline--fd51dfa5bf13---------------------------------------)[Felix Pappe](/@felix-pappe?source=post_page---byline--fd51dfa5bf13---------------------------------------)Follow

6분 읽기·6일 전·조회 78

<img src='https://miro.medium.com/v2/resize:fit:1400/0*zwaZDidQWNgj6Jcp' title='' width='700' height='467' />

*작은 로봇이 “cat(고양이)”, “dog(개)”, “banana(바나나)” 같은 단어를 이해하지 못해 당황하는 모습. 이는 기계가 인간 언어를 이해하는 데 직면하는 어려움을 보여줍니다. (이미지 제작: gpt-image-1)*

---

## 왜 원시 텍스트(raw text)는 기계에게 어려운가?

많은 머신러닝과 딥러닝 모델은 텍스트 정보를 직접 처리할 수 없습니다.

그 이유는, **원시 텍스트에 수학적 연산을 적용할 수 없기 때문**입니다.

예를 들어, “cat” + “dog” **= ?** 와 같은 연산을 숫자 계산(2 + 3 = 5)처럼 수행할 수는 없습니다.
이는 텍스트 데이터가 본질적인 수치적 관계가 없는 임의의 기호들의 나열이기 때문입니다.

하지만 웹상의 대부분의 데이터는 원시 텍스트 형태입니다. 이를 무시한다면, 가장 가치 있는 데이터 원천을 외면하는 셈입니다.

다행히도, 이를 해결할 방법이 있는데 바로 **임베딩(embedding)** 입니다.

---

## 임베딩(Embedding)이란?

임베딩은 데이터를 **벡터(vector)** 또는 **행렬(matrix)** 로 변환하는 개념입니다.
이 과정을 거치면 입력 정보를 의미적으로 담고 있는 **고정 길이 수치 벡터**가 생성됩니다.

오늘날의 고급 임베딩 알고리즘은 텍스트뿐만 아니라 이미지, 비디오, 음악까지 벡터로 변환할 수 있습니다.

<img src='https://miro.medium.com/v2/resize:fit:1400/1*e6Z_yRrmqLaEL_luWXGNyw.png' alt='A diagram showing the process of embedding various types of input data — text, image, video, and music — into numerical vector formats using dedicated embedding models. Each input type is illustrated with an icon, processed by a cube-shaped embedding model, and output as a column of numerical values labeled “Embedded Vectors.”' title='' width='700' height='700' />

*텍스트에서 벡터로: 임베딩 모델이 텍스트, 이미지, 비디오, 음악을 AI가 이해할 수 있는 수치 표현으로 변환하는 과정*

---

## 벡터와 클러스터란?

고급 알고리즘으로 들어가기 전에, 벡터와 클러스터를 간단히 이해해 봅시다.

예를 들어, 다섯 명의 사람이 있다고 가정해 봅시다. 이들이 **스포츠를 좋아하는 정도**와 **여행을 좋아하는 정도**를 0에서 9까지 점수로 평가한다고 합시다.

<img src='https://miro.medium.com/v2/resize:fit:1400/1*uNExWc4Enzhmjs9VK3eFxA.png' alt='An illustration of five cartoon-style people with distinct interests: a girl reading a book, a boy in casual clothes, a sporty man with a medal and soccer ball, a tourist woman with a map and camera, and a bearded traveler with luggage. The image represents how individuals with similar traits can be clustered together using vector embeddings in AI.' title='' width='700' height='350' />

*벡터 임베딩 시각화: 유사한 성향을 가진 사람들이 AI 클러스터링 모델에서 함께 묶이는 방식 (이미지 제작: gpt-image-1)*

각 사람은 자신의 특성을 나타내는 **벡터**로 표현될 수 있으며, 2차원 평면 위에 점으로 나타낼 수 있습니다.
이후 서로 비슷한 사람들을 묶으면, 이를 **클러스터(cluster)** 라고 부릅니다.

<img src='https://miro.medium.com/v2/resize:fit:1400/1*NWXBG1112zFbXcUTO9E6-w.png' alt='A 2D scatter plot showing five individuals — Lisa, Max, Hans, Li, and Carl — plotted based on their sport and travel preferences. The X-axis represents travel preferences and the Y-axis represents sport preferences, demonstrating how vectors can represent personal traits for clustering in AI.' title='' width='700' height='349' />

*여행과 스포츠 선호도를 기준으로 사람들을 그룹화하는 벡터 임베딩과 클러스터링의 이해*

---

## 워드 임베딩(Word Embeddings)

이제 같은 개념을 **단어**에 적용할 수 있습니다.

멀티디멘션(다차원) 벡터 공간에서 서로 가까이 위치한 단어들은 의미적으로 관련성이 있습니다.
이 과정의 목표는 데이터를 신경망이 이해할 수 있는 **수치적 형식**으로 변환하는 것입니다.

<img src='https://miro.medium.com/v2/resize:fit:1400/1*txWvd_cI5TTPqHgYIPJGlQ.png' alt='A 2D scatter plot showing word embeddings for fantasy-themed words: dragon, unicorn, wizard, castle, and princess. Plotted on the X-axis (first dimension) and Y-axis (second dimension), the chart illustrates how semantically related words group together in a vector space.' title='' width='700' height='335' />

*2차원 벡터 공간에서 의미적으로 연관된 단어들을 시각화한 워드 임베딩*

---

## 첫 번째 임베딩 알고리즘 코딩하기

이제 간단한 알고리즘인 **Bag-of-Words(BoW)** 를 Python으로 구현해 봅시다.

BoW에서는 문서, 문장, 단락을 단어의 **출현 횟수 벡터**로 표현합니다.

<img src='https://miro.medium.com/v2/resize:fit:1400/1*p6_rQXUhj7198PDpp-S3oA.png' alt='A paper bag labeled “Bag of Words” with colorful 3D words like “balls,” “cats,” “love,” “logs,” “playing,” and “with” popping out of it. The image visually represents the Bag-of-Words model, where words are treated as individual units for counting their frequency in a sentence or document.' title='' width='700' height='234' />

*Bag of Words 모델: 텍스트를 카운트 가능한 특징으로 변환하는 기본 임베딩 방식 (이미지 제작: gpt-image-1)*

---

## Bag-of-Words의 한계

BoW는 간단하지만, 실제 언어를 충분히 표현하기에는 한계가 있습니다.

* 영어 사전에만 60만 개 이상의 단어가 존재합니다.
* 시제 변화, 대명사 결합 등으로 벡터 차원은 기하급수적으로 커집니다.

따라서 BoW는 좋은 출발점이지만, 단순한 단어 빈도 세기를 넘어선 **더 발전된 임베딩 알고리즘**이 필요합니다.

---

## 다음 단계

대규모 언어 모델(LLM)은 학습 과정에서 자체적으로 임베딩을 생성합니다.
즉, BoW 같은 사전 학습 모델을 직접 사용하지 않습니다.

이 과정의 장점은, 임베딩이 특정 데이터와 작업에 최적화된다는 것입니다.

하지만 트랜스포머 기반 임베딩을 깊이 이해하기 위해서는 전통적인 방법들을 먼저 알아두는 것이 좋습니다.

다음 글에서는 대표적인 임베딩 알고리즘 두 가지를 다룰 예정입니다.

그러니 계속 호기심을 유지하시고, 다음 글에서 만나요!

---

[felix-pappe.medium.com/subscribe](http://felix-pappe.medium.com/subscribe) 🔔
[www.linkedin.com/in/felix-pappe](http://felix-pappe/) 🔗
[https://felixpappe.de](https://felixpappe.de/) 🌐
