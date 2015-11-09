# z3_loginDefaultEncrypt

## 0x01背景介绍
Vxworks-5.x、6.x使用函数loginDefaultEncrypt对明文密码进行哈希。然而该函数存在整形截断缺陷，导致其违背了密码学中的抗冲突性原则
。Christian和Kleist使用暴破法对其进行了破解，然而暴破法需要较长的时间。本代码使用Z3求解的方法直接解出明文密码。

## Z3介绍
Z3是微软研究院开发的一款约束求解器（SMT），用来检查一组约束公式的可满足性（satisfiability）并求解出符合约束条件的解。Z3在学术界应用广泛，例如符号执行，智能fuzz，路径分析等。目前Z3对python提供了API接口，使用十分方便。Z3的安装和介绍见参考资料。

## 使用说明
z3Cracker <ciphertext> <password_len>
  ciphertext: password string that has been hashed 
  password_len: a number between 8 to 40
Examples: 
	z3Cracker bRbQyzcy9b 8
	z3Cracker bbddRdzb9 22
	z3Cracker cdcS9bcQc 8
	z3Cracker See9cb9y99 9

## 总结
通过Z3破解有缺陷加密函数的方法具有较强的通用性，以此代码为模板稍加修改即可适用于其他不安全加密函数的破解。

## 参考资料

[施耐德PLC以太网模块固件后门引发的血案][1]

[施耐德PLC以太网模块固件后门引发的血案(二)][2]

[邪恶的0x4321][3]

[VxWorks 5.x源码][4]

[Christian和Kleist给出的爆破hash的代码以及lookup表][5]

[Z3入门][6]

[Z3安装][7]

[Z3 python API介绍][8]

[1]: http://mp.weixin.qq.com/s?__biz=MzA5OTMwMzY1NQ==&mid=207033762&idx=1&sn=e629b1db9f43937cba6d5707c707450d&scene=23&srcid=11052lU6PwhrrCHsh1r5goGp#rd
[2]: http://mp.weixin.qq.com/s?__biz=MzA5OTMwMzY1NQ==&mid=207094710&idx=1&sn=13fc594d15729bd7e001a48b90d827c4&scene=23&srcid=11052GJ08GApP8m9VedAhiQi#rd
[3]: http://mp.weixin.qq.com/s?__biz=MzA5OTMwMzY1NQ==&mid=400049207&idx=1&sn=a8c864a63c4a22664137ca96a7f5ce7f&scene=23&srcid=1105NAC90QqWu3Rv54FEA44J#rd
[4]: https://github.com/olerem/vxworks5
[5]: https://github.com/cvonkleist/vxworks_hash
[6]: http://rise4fun.com/z3/tutorial/guide
[7]: https://github.com/Z3Prover/z3
[8]: http://www.cs.tau.ac.il/~msagiv/courses/asv/z3py/guide-examples.htm
