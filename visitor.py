
class Visitor(object):

	@classmethod
	def register(celf, clazzes, attrs=(None,)):
		assert celf != Visitor, 'Subclass Visitor instead.'
		if '_visitors' not in celf.__dict__:
			celf._visitors = {}
		if type(clazzes) != tuple:
			clazzes = (clazzes,)
		if type(attrs) == str:
			attrs = (attrs,)
		def wrapper(method):
			assert method.__name__ == 'visit'
			done = []
			for clazz in clazzes:
				if clazz in done: continue # Support multiple names of a clazz
				done.append(clazz)
				_visitors = celf._visitors.setdefault(clazz, {})
				for attr in attrs:
					assert attr not in _visitors, \
						"Oops, class '%s' has visitor function for '%s' defined already." % (clazz.__name__, attr)
					_visitors[attr] = method
			return None
		return wrapper

	@classmethod
	def _visitorsFor(celf, thing, _default={}):
		typ = type(thing)

		for celf in celf.mro():

			_visitors = getattr(celf, '_visitors', None)
			if _visitors is None:
				break;

			m = celf._visitors.get(typ, None)
			if m is not None:
				return m

		return _default

	def visitObject(self, obj, *args, **kwargs):
		keys = sorted(vars(obj).keys())
		_visitors = self._visitorsFor(obj)
		defaultVisitor = _visitors.get('*', self.__class__.visit)
		for key in keys:
			value = getattr(obj, key)
			visitorFunc = _visitors.get(key)
			if visitorFunc is None:
				defaultVisitor(self, value, *args, **kwargs)
			else:
				visitorFunc(self, obj, key, value, *args, **kwargs)

	def visitList(self, obj, *args, **kwargs):
		for value in obj:
			self.visit(value, values)

	def visit(self, obj, *args, **kwargs):
		visitorFunc = self._visitorsFor(obj).get(None, None)
		if visitorFunc is not None:
			if visitorFunc(self, obj, *args, **kwargs) == False:
			  return
		if hasattr(obj, '__dict__'):
			self.visitObject(obj, *args, **kwargs)
		elif isinstance(obj, list):
			self.visitList(obj, *args, **kwargs)


class DFS(Visitor):

	def visit(self, obj, arg):
		print("generic", type(obj))
		super().visit(obj, arg)

class A:
	def __init__(self):
		self.count = 0

class B(A):
	pass

class C:
	def __init__(self):
		self.a = A()
		self.b = B()

@DFS.register(A)
def visit(visitor, obj, arg):
	print("A")

@DFS.register(A, 'count')
def visit(visitor, obj, attr, value, arg):
	setattr(obj, attr, arg)
	print("A", attr)

@DFS.register(B)
def visit(visitor, obj, arg):
	print("B")

dfs = DFS()
dfs.visit(C(), 5)

# generic C
# A
# A visited
# B
# generic B visited
