from pytest import raises


class TestTypeHints:
    def setup_class(cls):
        import cppyy

        cppyy.cppdef(
            r"""
            namespace TypeHints {
                int x = 10;
                template <typename T>
                struct MyTKlass{
                    T obj;
                };
                struct MyKlass {
                    std::string name = "MyKlass";
                    bool flag = false;
                    std::vector<int> array = {};
                    float callme(std::string a, bool b, std::vector<int> c) { return 0.0f; }
                    template <typename T>
                    T callme(T v) { return v; }
                };
                typedef MyKlass Klass;
                typedef MyTKlass<float> KlassFloat;
                float fn(std::string a, bool b, std::vector<int> c) { return 0.0f; }
                template <typename T>
                T tmpl_fn(T v) { return v; }
            } // namespace TypeHints
            int x = 10;
            double y = 10;
            unsigned short z = 10;
            char a = 'a';
            signed char sa = 'a';
            unsigned char usa = 'a';
            template <typename T>
            struct MyTKlass{
                T obj;
            };
            struct MyKlass {
                std::string name = "MyKlass";
                bool flag = false;
                std::vector<int> array = {};
                float callme(std::string a, bool b, std::vector<int> c) { return 0.0f; }
                template <typename T>
                T callme(T v) { return v; }
            };
            float callme(std::string a, bool b, std::vector<int> c) { return 0.0f; }
            template <typename T>
            T tmpl_fn(T v) { return v; }
            typedef MyKlass Klass;
            typedef MyTKlass<float> KlassFloat;
        """
        )

    def test_invalids(self):
        from cppyy import gbl, generate_typehints

        typehint = generate_typehints("x")
        assert "x: int\n" == typehint
        typehint = generate_typehints("y")
        assert "y: float\n" == typehint
        typehint = generate_typehints("z")
        assert "z: int\n" == typehint
        typehint = generate_typehints("a")
        assert "a: str\n" == typehint
        typehint = generate_typehints("sa")
        assert "sa: int\n" == typehint
        typehint = generate_typehints("usa")
        assert "usa: int\n" == typehint

        with raises(NotImplementedError) as err:
            generate_typehints("MyKlass")
        assert "class" in str(err)

        typehint = generate_typehints("callme")
        assert (
            '@overload\ndef callme (a: "std.string", b: bool, c: "std.vector[int]") -> float: ...\n'
            == typehint
        )

        typehint = generate_typehints("Klass")
        assert "Klass = MyKlass\n" == typehint

        typehint = generate_typehints("KlassFloat")
        assert "KlassFloat = \"MyTKlass[float]\"\n" == typehint

        with raises(NotImplementedError) as err:
            generate_typehints("MyTKlass")

        with raises(NotImplementedError) as err:
            generate_typehints("TypeHints")
        assert "namespace" in str(err)

        with raises(TypeError) as err:
            generate_typehints("unknown")
        assert "Unknown Type" in str(err)

        with raises(TypeError) as err:
            generate_typehints("TypeHints::x")
