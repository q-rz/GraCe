from inc.benchmarks import *
from inc.evaluator import *

args = Dict(
    seed = 123456,
    save_dir = 'output',
    benchmark = 'attack',
    max_steps = 100,
    max_queries = 20000,
    
    lr = 0.001,
    eps = 1e-6,
    num_samples = 199,
)

class Optimizer(BaseOptimizer):
    NAME = 'ZO-signSGD'
    def init(self):
        self.d = self.bm.func.d
        self.s = self.bm.func.s
    def step(self):
        x0 = self.x
        y0 = self.y
        Z = np.random.normal(size = (args.num_samples, self.d))
        U = Z / np.sqrt(np.square(Z).sum(axis = 1, keepdims = True))
        yU = self.bm.query(x0 + args.eps * U)
        grad = (((yU - y0)[:, None] / args.eps) * U).mean(axis = 0) * self.d
        grad = np.sign(grad)
        return self.update(x0 - args.lr * grad)

bm_list = get_benchmark(args.benchmark)
for bm in bm_list:
    evaluator = Evaluator(bm = bm, opt_cls = Optimizer, max_steps = args.max_steps, max_queries = args.max_queries, seed = args.seed, save_dir = args.save_dir)
    evaluator.main()