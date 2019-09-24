```mermaid
graph TB;
A[项目立项]
B[需求]
C[原型设计]
D[架构设计]
E[数据库设计]
F[模块代码和单元测试]
G[代码整合]
H[UI设计]
I[前端设计]
J[集成测试]
K[网站发布]

A-->B
B-->C
C-->D

D-->E
E-->F
F-->G
G-->J
J-->K

C-->H
H-->I
I-->G
```
