Folder <pgmpy_Python>
 * PyCharm에서 pgmpy 라이브러리를 이용해 Dynamic Bayesian Network-based smoke distribution model을 계산하기 위해 작성했던 코드들입니다.
  - Folder <data> : 코드를 테스트하기 위해 사용한 data들
  - Folder <opensource_gbxml> : 그래프(노드 간 연결관계)를 생성하기 위해 사용한 깃허브 오픈소스 라이브러리 gbxml 코드 (출처: )
  - graphDBN1.py | gbxml 라이브러리를 이용해 markov chain model에 이용할 그래프 생성하는 코드
  - transientDBN.py, transientDBN_modify.py | graphDBN1에서 생성한 건물의 room(node) 간 연결 관계를 기반으로 DBN을 계산하는 코드

* PGMPY 라이브러리로 연구를 가장 먼저 시작할 수 있었으나 라이브러리의 성능 한계(계산할 수 있는 노드의 최대 개수 등에 한계가 있었음), 라이브러리 이해의 어려움에 의한 코드 미비 등으로 개선의 필요성을 느낌

Folder <pyAgrum_JupyterNotebook>
 ※ 추후 코드를 정리하는 작업이 필요함. rough 버전이니 참고만 부탁드립니다.

 * pyAgrum 라이브러리를 이용해 작성한 코드들입니다.
 * pgmpy 라이브러리를 이용했을 때의 성능 한계, 라이브러리 이해에 대한 자료 부족 등을 극복할 수 있었음.
 * 해당 코드들로 재진행한 연구로 SCI 작성, 투고 중에 있습니다.
