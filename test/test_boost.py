import py, os, sys
from pytest import mark, raises, skip
from .support import setup_make, IS_CLANG_REPL, IS_MAC_X86, IS_MAC_ARM

noboost = False
if not (os.path.exists(os.path.join(os.path.sep, 'usr', 'include', 'boost')) or \
        os.path.exists(os.path.join(os.path.sep, 'usr', 'local', 'include', 'boost'))):
    noboost = True


@mark.skipif(noboost == True, reason="boost not found")
class TestBOOSTANY:
    def setup_class(cls):
        import cppyy

        cppyy.include('boost/any.hpp')

    @mark.skipif((IS_MAC_ARM or IS_MAC_X86), reason="Fails to include boost on OS X")
    def test01_any_class(self):
        """Availability of boost::any"""

        import cppyy

        assert cppyy.gbl.boost.any

        from cppyy.gbl import std
        from cppyy.gbl.boost import any

        assert std.list[any]

    @mark.skip
    def test02_any_usage(self):
        """boost::any assignment and casting"""

        import cppyy

        assert cppyy.gbl.boost

        from cppyy.gbl import std, boost

        val = boost.any()
        # test both by-ref and by rvalue
        v = std.vector[int]()
        val.__assign__(v)
        val.__assign__(std.move(std.vector[int](range(100))))
        assert val.type() == cppyy.typeid(std.vector[int])

        extract = boost.any_cast[std.vector[int]](val)
        assert type(extract) is std.vector[int]
        assert len(extract) == 100
        extract += range(100)
        assert len(extract) == 200

        val.__assign__(std.move(extract))   # move forced
        #assert len(extract) == 0      # not guaranteed by the standard

        # TODO: we hit boost::any_cast<int>(boost::any* operand) instead
        # of the reference version which raises
        boost.any_cast.__useffi__ = False
        try:
          # raises(Exception, boost.any_cast[int], val)
            assert not boost.any_cast[int](val)
        except Exception:
          # getting here is good, too ...
            pass

        extract = boost.any_cast[std.vector[int]](val)
        assert len(extract) == 200


@mark.skipif(((noboost == True) or IS_MAC_ARM or IS_MAC_X86), reason="boost not found")
class TestBOOSTOPERATORS:
    def setup_class(cls):
        import cppyy

        cppyy.include('boost/operators.hpp')

    def test01_ordered(self):
        """ordered_field_operators as base used to crash"""

        import cppyy

        try:
            cppyy.include("gmpxx.h")
        except ImportError:
            skip("gmpxx not installed")
        cppyy.cppdef("""
            namespace boost_test {
               class Derived : boost::ordered_field_operators<Derived>, boost::ordered_field_operators<Derived, mpq_class> {};
            }
        """)

        assert cppyy.gbl.boost_test.Derived


@mark.skipif(noboost == True, reason="boost not found")
class TestBOOSTVARIANT:
    def setup_class(cls):
        import cppyy

        cppyy.include("boost/variant/variant.hpp")
        cppyy.include("boost/variant/get.hpp")

    @mark.skip
    def test01_variant_usage(self):
        """boost::variant usage"""

      # as posted on stackoverflow as example
        import cppyy

        cpp   = cppyy.gbl
        std   = cpp.std
        boost = cpp.boost

        cppyy.cppdef("""namespace BV {
          class A { };
          class B { };
          class C { }; } """)

        VariantType = boost.variant['BV::A, BV::B, BV::C']
        VariantTypeList = std.vector[VariantType]

        v = VariantTypeList()

        v.push_back(VariantType(cpp.BV.A()))
        assert v.back().which() == 0
        v.push_back(VariantType(cpp.BV.B()))
        assert v.back().which() == 1
        v.push_back(VariantType(cpp.BV.C()))
        assert v.back().which() == 2

        assert type(boost.get['BV::A'](v[0])) == cpp.BV.A

        # Trying to raise this exception seg faults, by trying to execute an unfit instantiation.
        # This comes from `Instantiate` obtaining a single handle and providing a result
        # The same issue happens with trying `BestOverloadFunctionMatch` first since the candidate set is single
        raises(Exception, boost.get['BV::B'], v[0])
        assert type(boost.get['BV::B'](v[1])) == cpp.BV.B
        assert type(boost.get['BV::C'](v[2])) == cpp.BV.C


@mark.skipif(((noboost == True) or IS_MAC_ARM or IS_MAC_X86), reason="boost not found")
class TestBOOSTERASURE:
    def setup_class(cls):
        import cppyy

        cppyy.include("boost/type_erasure/any.hpp")
        cppyy.include("boost/type_erasure/member.hpp")
        cppyy.include("boost/mpl/vector.hpp")

    def test01_erasure_usage(self):
        """boost::type_erasure usage"""

        import cppyy

        cppyy.cppdef("""
            BOOST_TYPE_ERASURE_MEMBER((has_member_f), f, 0)

            using LengthsInterface = boost::mpl::vector<
                boost::type_erasure::copy_constructible<>,
                has_member_f<std::vector<int>() const>>;

            using Lengths = boost::type_erasure::any<LengthsInterface>;

            struct Unerased {
                std::vector<int> f() const { return std::vector<int>{}; }
            };

            Lengths lengths() {
                return Unerased{};
            }
        """)

        assert cppyy.gbl.lengths() is not None
